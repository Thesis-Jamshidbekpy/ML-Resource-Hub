"""
Populate the database with realistic demo records for every main table.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --count 30
    python manage.py seed_demo_data --fresh
"""

from __future__ import annotations

import random
from itertools import cycle

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from apps.accounts.models import FavoriteAlgorithm, Profile, RecentlyViewedAlgorithm
from apps.algorithms.models import Algorithm, Comment, Rating
from apps.dashboard.seed_catalog import (
    ACADEMIC_INTERESTS,
    ADVANTAGES,
    ADVANTAGES_UZ,
    ALGORITHM_SPECS,
    APPLICATIONS,
    APPLICATIONS_UZ,
    AUTHORS,
    COMMENT_TEXTS,
    COMMENT_TEXTS_UZ,
    COMPLEXITY,
    COMPLEXITY_UZ,
    DEMO_USER_PASSWORD,
    DESCRIPTION_TEMPLATE,
    DESCRIPTION_TEMPLATE_UZ,
    DISADVANTAGES,
    DISADVANTAGES_UZ,
    INSTITUTIONS,
    MATH_FOUNDATION,
    MATH_FOUNDATION_UZ,
    RESOURCE_TITLES,
)
from apps.resources.models import Resource, ResourceBookmark

User = get_user_model()

DEMO_USER_PREFIX = "demo_student_"
DEMO_GROUP_NAMES = [
    "ML Students",
    "ML Instructors",
    "Researchers",
    "Content Moderators",
    "Thesis Reviewers",
]


class Command(BaseCommand):
    help = "Seed realistic demo data (default: 30 rows per main table)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=30,
            help="Number of records to create per table (default: 30).",
        )
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete previously seeded demo users and demo algorithms first.",
        )
        parser.add_argument(
            "--password",
            type=str,
            default=DEMO_USER_PASSWORD,
            help=f"Password for generated demo users (default: {DEMO_USER_PASSWORD}).",
        )

    def handle(self, *args, **options):
        count: int = options["count"]
        password: str = options["password"]

        if count < 1:
            self.stderr.write(self.style.ERROR("--count must be at least 1."))
            return

        if options["fresh"]:
            self._clear_demo_data()

        with transaction.atomic():
            groups = self._seed_groups(count)
            users = self._seed_users(count, password)
            self._assign_groups(users, groups)
            profiles = self._seed_profiles(users)
            algorithms = self._seed_algorithms(count)
            resources = self._seed_resources(count, algorithms)
            comments = self._seed_comments(count, users, algorithms)
            ratings = self._seed_ratings(count, users, algorithms)
            favorites = self._seed_favorites(count, users, algorithms)
            bookmarks = self._seed_bookmarks(count, users, resources)
            recent = self._seed_recent_views(count, users, algorithms)

        self.stdout.write(self.style.SUCCESS("Demo data seeding completed."))
        self.stdout.write(f"  Groups:              {len(groups)}")
        self.stdout.write(f"  Users:               {len(users)}")
        self.stdout.write(f"  Profiles:            {len(profiles)}")
        self.stdout.write(f"  Algorithms:          {len(algorithms)}")
        self.stdout.write(f"  Resources:           {len(resources)}")
        self.stdout.write(f"  Comments:            {len(comments)}")
        self.stdout.write(f"  Ratings:             {len(ratings)}")
        self.stdout.write(f"  Favorite algorithms: {len(favorites)}")
        self.stdout.write(f"  Resource bookmarks:  {len(bookmarks)}")
        self.stdout.write(f"  Recent views:        {len(recent)}")
        self.stdout.write("")
        self.stdout.write(f"Demo login example: {DEMO_USER_PREFIX}01 / {password}")

    def _clear_demo_data(self):
        demo_users = User.objects.filter(username__startswith=DEMO_USER_PREFIX)
        demo_slugs = [spec[2] for spec in ALGORITHM_SPECS]
        deleted_algos = Algorithm.objects.filter(slug__in=demo_slugs).count()
        deleted_users = demo_users.count()
        demo_users.delete()
        Algorithm.objects.filter(slug__in=demo_slugs).delete()
        self.stdout.write(
            self.style.WARNING(
                f"Cleared {deleted_users} demo users and {deleted_algos} catalog algorithms."
            )
        )

    def _seed_groups(self, count: int) -> list[Group]:
        target = min(count, len(DEMO_GROUP_NAMES))
        groups: list[Group] = []
        for name in DEMO_GROUP_NAMES[:target]:
            group, _ = Group.objects.get_or_create(name=name)
            groups.append(group)
        if count > target:
            for index in range(target, count):
                name = f"ML Cohort {index + 1:02d}"
                group, _ = Group.objects.get_or_create(name=name)
                groups.append(group)
        return groups

    def _seed_users(self, count: int, password: str) -> list:
        users = []
        for index in range(1, count + 1):
            username = f"{DEMO_USER_PREFIX}{index:02d}"
            email = f"{username}@mlresourcehub.demo"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": "Demo",
                    "last_name": f"Student {index:02d}",
                    "is_active": True,
                },
            )
            if created:
                user.set_password(password)
                user.save(update_fields=["password"])
            users.append(user)
        return users

    def _assign_groups(self, users: list, groups: list[Group]) -> None:
        if not groups:
            return
        for user, group in zip(users, cycle(groups)):
            user.groups.add(group)

    def _seed_profiles(self, users: list) -> list[Profile]:
        profiles = []
        for index, user in enumerate(users):
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.bio = (
                f"Demo student account focused on machine learning coursework and thesis preparation. "
                f"Interested in practical model evaluation and reproducible experiments."
            )
            profile.institution = INSTITUTIONS[index % len(INSTITUTIONS)]
            profile.academic_interest = ACADEMIC_INTERESTS[index % len(ACADEMIC_INTERESTS)]
            profile.save()
            profiles.append(profile)
        return profiles

    def _seed_algorithms(self, count: int) -> list[Algorithm]:
        algorithms: list[Algorithm] = []
        specs = ALGORITHM_SPECS[:count]
        if count > len(ALGORITHM_SPECS):
            for extra in range(len(ALGORITHM_SPECS), count):
                name = f"Custom ML Method {extra + 1}"
                specs.append(
                    (
                        name,
                        f"Maxsus ML usuli {extra + 1}",
                        slugify(name),
                        "classification",
                        "Research Prototype",
                        "Tadqiqot prototipi",
                    )
                )

        for index, (name, name_uz, slug, category, algo_type, algo_type_uz) in enumerate(specs):
            algorithm, created = Algorithm.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "name_uz": name_uz,
                    "category": category,
                    "algorithm_type": algo_type,
                    "algorithm_type_uz": algo_type_uz,
                    "description": DESCRIPTION_TEMPLATE.format(name=name),
                    "description_uz": DESCRIPTION_TEMPLATE_UZ.format(name_uz=name_uz),
                    "mathematical_foundation": MATH_FOUNDATION,
                    "mathematical_foundation_uz": MATH_FOUNDATION_UZ,
                    "advantages": ADVANTAGES,
                    "advantages_uz": ADVANTAGES_UZ,
                    "disadvantages": DISADVANTAGES,
                    "disadvantages_uz": DISADVANTAGES_UZ,
                    "applications": APPLICATIONS,
                    "applications_uz": APPLICATIONS_UZ,
                    "complexity": COMPLEXITY,
                    "complexity_uz": COMPLEXITY_UZ,
                    "view_count": random.randint(40, 420),
                },
            )
            if not created:
                algorithm.view_count = max(algorithm.view_count, random.randint(40, 420))
                algorithm.save(update_fields=["view_count"])
            algorithms.append(algorithm)
        return algorithms

    def _seed_resources(self, count: int, algorithms: list[Algorithm]) -> list[Resource]:
        resources: list[Resource] = []
        titles = list(RESOURCE_TITLES)
        if count > len(titles):
            for extra in range(len(titles), count):
                titles.append((f"ML Study Resource {extra + 1}", f"ML o'quv resursi {extra + 1}", "article"))

        for index in range(count):
            title, title_uz, resource_type = titles[index % len(titles)]
            algorithm = algorithms[index % len(algorithms)]
            author = AUTHORS[index % len(AUTHORS)]
            resource, _ = Resource.objects.get_or_create(
                algorithm=algorithm,
                title=title,
                defaults={
                    "title_uz": title_uz,
                    "resource_type": resource_type,
                    "author": author,
                    "author_uz": author,
                    "description": (
                        f"{title} provides structured material for studying {algorithm.name} "
                        f"with examples, references, and practical exercises."
                    ),
                    "description_uz": (
                        f"{title_uz} {algorithm.name_uz or algorithm.name} bo'yicha nazariya va amaliy mashqlar beradi."
                    ),
                    "external_url": f"https://example.edu/ml-resources/{slugify(title)}",
                    "download_count": random.randint(5, 180),
                },
            )
            resources.append(resource)
        return resources

    def _seed_comments(self, count: int, users: list, algorithms: list[Algorithm]) -> list[Comment]:
        comments: list[Comment] = []
        for index in range(count):
            user = users[index % len(users)]
            algorithm = algorithms[index % len(algorithms)]
            text = COMMENT_TEXTS[index % len(COMMENT_TEXTS)]
            uz = COMMENT_TEXTS_UZ[index % len(COMMENT_TEXTS_UZ)]
            comment = Comment.objects.create(
                user=user,
                algorithm=algorithm,
                text=f"{text} ({uz})",
            )
            comments.append(comment)
        return comments

    def _seed_ratings(self, count: int, users: list, algorithms: list[Algorithm]) -> list[Rating]:
        ratings: list[Rating] = []
        pairs = [(users[i % len(users)], algorithms[i % len(algorithms)]) for i in range(count)]
        for user, algorithm in pairs:
            rating, _ = Rating.objects.update_or_create(
                user=user,
                algorithm=algorithm,
                defaults={"score": random.randint(3, 5)},
            )
            ratings.append(rating)
        return ratings

    def _seed_favorites(self, count: int, users: list, algorithms: list[Algorithm]) -> list[FavoriteAlgorithm]:
        favorites: list[FavoriteAlgorithm] = []
        for index in range(count):
            user = users[index % len(users)]
            algorithm = algorithms[(index + 3) % len(algorithms)]
            favorite, _ = FavoriteAlgorithm.objects.get_or_create(user=user, algorithm=algorithm)
            favorites.append(favorite)
        return favorites

    def _seed_bookmarks(self, count: int, users: list, resources: list[Resource]) -> list[ResourceBookmark]:
        bookmarks: list[ResourceBookmark] = []
        for index in range(count):
            user = users[index % len(users)]
            resource = resources[(index + 5) % len(resources)]
            bookmark, _ = ResourceBookmark.objects.get_or_create(user=user, resource=resource)
            bookmarks.append(bookmark)
        return bookmarks

    def _seed_recent_views(
        self, count: int, users: list, algorithms: list[Algorithm]
    ) -> list[RecentlyViewedAlgorithm]:
        recent: list[RecentlyViewedAlgorithm] = []
        now = timezone.now()
        for index in range(count):
            user = users[index % len(users)]
            algorithm = algorithms[(index + 7) % len(algorithms)]
            item, _ = RecentlyViewedAlgorithm.objects.update_or_create(
                user=user,
                algorithm=algorithm,
                defaults={"last_viewed_at": now},
            )
            recent.append(item)
        return recent
