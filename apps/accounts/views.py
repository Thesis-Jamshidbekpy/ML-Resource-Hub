"""Views supporting authentication, profiles, and personalized lists."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import CustomAuthenticationForm, ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import FavoriteAlgorithm


class CustomLoginView(LoginView):
    """Render the platform-specific Bootstrap login page."""

    authentication_form = CustomAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Terminate the active session and return to the landing page."""

    next_page = reverse_lazy("dashboard:home")


class RegisterView(CreateView):
    """Register new users with Django's authentication backend."""

    form_class = SignUpForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, _("Your account has been created successfully."))
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """Show the user's profile, favorites, bookmarks, and recent activity."""

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["favorite_algorithms"] = (
            FavoriteAlgorithm.objects.select_related("algorithm")
            .filter(user=user)
            .order_by("-created_at")
        )
        context["bookmarked_resources"] = (
            user.resource_bookmarks.select_related("resource", "resource__algorithm")
            .all()
            .order_by("-created_at")
        )
        context["recently_viewed"] = (
            user.recently_viewed_algorithms.select_related("algorithm")
            .all()
            .order_by("-last_viewed_at")[:8]
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit extended profile data in a dedicated view."""

    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("user_form", UserUpdateForm(instance=self.request.user))
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Profile details updated successfully."))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, View):
    """Persist core user identity fields from the profile edit page."""

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, _("Your account information has been updated."))
            return redirect("accounts:profile")
        messages.error(request, _("Please correct the highlighted fields and try again."))
        return render(
            request,
            "accounts/profile_edit.html",
            {"form": profile_form, "user_form": form},
        )
