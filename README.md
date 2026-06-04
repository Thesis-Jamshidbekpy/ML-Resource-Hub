# ML Resource Hub

ML Resource Hub is a complete Django web application for cataloging machine learning algorithms and the educational resources associated with them. It is designed as a final-year university graduation project and demonstrates a professional multi-app Django architecture with authentication, admin customization, REST APIs, PostgreSQL configuration, Bootstrap 5 UI, fixtures, and scalable domain modeling.

## What This Project Can Do (English)

ML Resource Hub is a knowledge management and discovery platform for machine learning education. It allows users to collect, organize, search, evaluate, and study machine learning algorithms together with their learning materials in one centralized system.

### Main Capabilities

- Store machine learning algorithms with structured academic information such as description, mathematical foundation, advantages, disadvantages, applications, and complexity
- Attach learning resources to each algorithm, including books, articles, research papers, videos, documentation, and datasets
- Let users register, log in, manage profiles, comment on algorithms, rate algorithms, save favorites, and bookmark resources
- Help users discover content through search, category filters, resource type filters, and popularity/date ordering
- Track platform activity through view counters, download counters, recently viewed algorithms, and dashboard statistics
- Provide Django admin tools for managing content, users, comments, ratings, and educational resources
- Expose REST API endpoints for integration with mobile apps, frontend clients, or other academic systems

### Business Logic

The business logic of the project is based on the relationship between `algorithms`, `resources`, and `users`.

- `Algorithms` are the main knowledge entities in the system
- Each `algorithm` can have many `resources`
- Users can interact with algorithms by writing `comments`, giving `ratings`, and adding them to `favorites`
- Users can interact with resources by saving `bookmarks` and increasing the `download counter` when accessing material
- The system calculates popularity using engagement signals such as views, ratings, and saved items
- The dashboard aggregates platform data to support academic presentation, admin monitoring, and content analysis
- Recently viewed records help users continue their learning journey from where they left off
- Related algorithms help users discover similar techniques within the same category

### What You Can Use This Project For

- Final-year university graduation project
- Thesis demonstration or viva presentation
- Educational portal for machine learning students
- Internal learning platform for a university department or training center
- Curated repository of ML study materials for teachers, mentors, or self-learners
- Backend foundation for a larger AI learning platform or mobile application
- Research resource catalog for organizing algorithm-specific references

## Loyiha Nima Qila Oladi (O'zbekcha)

ML Resource Hub bu mashinali o'qitish bo'yicha algoritmlar va ularga tegishli o'quv materiallarini bitta markazlashgan tizimda saqlash, tartiblash, qidirish va o'rganish uchun yaratilgan veb platformadir.

### Asosiy Imkoniyatlari

- Mashinali o'qitish algoritmlarini tavsifi, matematik asosi, afzalliklari, kamchiliklari, qo'llanilish sohalari va murakkabligi bilan birga saqlaydi
- Har bir algoritmga kitoblar, maqolalar, ilmiy ishlar, videolar, dokumentatsiyalar va datasetlarni biriktirish imkonini beradi
- Foydalanuvchilar ro'yxatdan o'tishi, tizimga kirishi, profilini boshqarishi, izoh yozishi, baho berishi, sevimlilariga qo'shishi va resurslarni bookmark qilishi mumkin
- Algoritm nomi, kategoriya va resurs turi bo'yicha qidirish hamda mashhurlik yoki sana bo'yicha saralashni qo'llab-quvvatlaydi
- Ko'rishlar soni, yuklab olishlar soni, so'nggi ko'rilgan algoritmlar va dashboard statistikasi orqali tizim faoliyatini kuzatadi
- Django Admin orqali algoritmlar, resurslar, foydalanuvchilar, izohlar va baholarni boshqarish imkonini beradi
- REST API orqali boshqa frontend, mobil ilova yoki akademik tizimlarga ulanish imkoniyatini beradi

### Biznes Logikasi

Loyihaning biznes logikasi `algorithms`, `resources` va `users` o'rtasidagi bog'lanishlarga asoslangan.

- `Algorithm` tizimdagi asosiy bilim obyektidir
- Har bir `algorithm` ga bir nechta `resource` bog'lanishi mumkin
- Foydalanuvchi algoritmga `comment` yozadi, `rating` beradi va uni `favorite` ga saqlaydi
- Foydalanuvchi resursni `bookmark` qiladi va resursga kirganda `download counter` oshadi
- Tizim mashhurlikni ko'rishlar soni, baholar va foydalanuvchi faolligi asosida baholaydi
- Dashboard umumiy statistikani yig'ib beradi va admin yoki taqdimot uchun qulay ko'rinish yaratadi
- Recently viewed funksiyasi foydalanuvchiga oldin ko'rgan algoritmlarini tez topishga yordam beradi
- Related algorithms funksiyasi bir xil kategoriyadagi o'xshash algoritmlarni tavsiya qiladi

### Ushbu Loyihadan Nima Uchun Foydalanish Mumkin

- Bitiruv malakaviy loyiha sifatida
- Diplom ishi yoki himoya taqdimoti uchun
- Mashinali o'qitish bo'yicha o'quv portal sifatida
- Universitet, o'quv markazi yoki laboratoriya ichki ta'lim platformasi sifatida
- O'qituvchilar va talabalar uchun ML resurslarini tartibli katalog qilish tizimi sifatida
- Kelajakda mobil ilova yoki katta AI ta'lim platformasi uchun backend asos sifatida
- Algoritmlar bo'yicha ilmiy manbalarni jamlash va boshqarish tizimi sifatida

## Features

- User registration, login, logout, and profile management
- Machine learning algorithm catalog with categories, detail pages, comments, ratings, view counters, and related algorithms
- Resource library for books, articles, research papers, videos, documentation, and datasets
- Search and filtering by algorithm name, category, and resource type
- Favorites for algorithms and bookmarks for resources
- Recently viewed algorithm tracking
- Dashboard with total algorithms, total resources, total users, most viewed algorithms, and latest resources
- Django admin customization for algorithms, resources, users, comments, and ratings
- Django REST Framework API for algorithms, resources, categories, comments, and ratings
- PostgreSQL-ready configuration with Docker Compose support

## Technology Stack

- Python 3.13+
- Django 6.0.6
- django-jazzmin (AdminLTE admin theme)
- Django REST Framework
- PostgreSQL
- Bootstrap 5
- Pillow
- django-filter

## Project Structure

```text
ML-Resource-Hub/
├── apps/
│   ├── accounts/
│   ├── algorithms/
│   ├── dashboard/
│   └── resources/
├── config/
├── fixtures/
├── static/
├── templates/
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## Domain Overview

### Core Apps

- `apps/accounts`: registration, login/logout integration, profile management, favorites, and recently viewed algorithms
- `apps/algorithms`: algorithm records, comments, ratings, search, popularity ordering, and REST endpoints
- `apps/resources`: resource records, bookmarks, download tracking, and REST endpoints
- `apps/dashboard`: homepage, platform analytics dashboard, and unified search results

### Main Models

- `Algorithm`
- `Comment`
- `Rating`
- `Resource`
- `ResourceBookmark`
- `Profile`
- `FavoriteAlgorithm`
- `RecentlyViewedAlgorithm`

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ML-Resource-Hub
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```

Example configuration:

```env
DJANGO_SECRET_KEY=change-me-for-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=ml_resource_hub
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Note: if PostgreSQL variables are not provided, the project falls back to SQLite for quick local smoke testing.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Load sample data

```bash
python manage.py loaddata fixtures/sample_users.json fixtures/sample_content.json
```

Demo user credentials from the fixtures:

- Username: `demo_student`
- Password: `DemoPass123!`

### 7b. Seed 30 realistic rows per table (optional)

After migrations, populate every main table with demo content (algorithms, resources, users, comments, ratings, favorites, bookmarks, recent views):

```bash
python manage.py seed_demo_data
python manage.py seed_demo_data --count 30
python manage.py seed_demo_data --fresh
```

Generated demo logins:

- Usernames: `demo_student_01` … `demo_student_30`
- Password: `DemoPass123!` (override with `--password`)

### 8. Start the development server

```bash
python manage.py runserver
```

Application URLs:

- Web app: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Docker Compose Setup

1. Copy `.env.example` to `.env`
2. Start the containers:

```bash
docker compose up --build
```

The `web` service runs migrations automatically and serves the application on port `8000`.

### Docker: `password authentication failed for user "postgres"`

PostgreSQL stores the password only when the data volume is **first created**. If you later change `POSTGRES_PASSWORD` in `.env`, the running database still uses the old password.

**Fix (resets all DB data):**

```bash
docker compose down -v
docker compose up --build
```

Ensure `.env` matches `.env.example` for Docker (or set the same values in both `db` and `web`):

```env
POSTGRES_DB=ml_resource_hub
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Then seed demo data inside the container:

```bash
docker compose exec web python manage.py seed_demo_data
```

### Docker build: `registry-1.docker.io: no such host`

This is a **DNS/network issue inside Docker Desktop**, not a broken `Dockerfile`. The image tag `python:3.13-slim` is valid.

1. **Pull the base image on the host first** (often fixes the next build):

```bash
docker pull python:3.13-slim
docker pull postgres:17
docker compose build
docker compose up
```

2. **Set DNS for Docker Desktop** (macOS): Docker Desktop → **Settings** → **Docker Engine**, add:

```json
{
  "dns": ["8.8.8.8", "1.1.1.1"]
}
```

Apply & Restart, then run `docker compose up --build` again.

3. **Check VPN / proxy**: disable VPN temporarily or configure Docker Desktop proxy if your network requires it.

4. **Run without Docker** (local venv works the same):

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

## REST API Endpoints

Base API path: `/api/`

- `/api/algorithms/`
- `/api/resources/`
- `/api/categories/`
- `/api/comments/`
- `/api/ratings/`

### Example API Usage

```bash
curl http://127.0.0.1:8000/api/algorithms/
curl http://127.0.0.1:8000/api/resources/
curl http://127.0.0.1:8000/api/categories/
```

## Search and Filtering

### Algorithm Search

- Search by algorithm name
- Filter by category
- Order by name, popularity, or latest date

### Resource Search

- Search by resource title
- Filter by resource type
- Order by popularity, latest date, or title

### Unified Search Page

- Search algorithms and resources from one page
- Optional category and resource type filters

## Admin Features

The admin panel uses **django-jazzmin** with a disciplined color palette:

- **Black** — sidebar and structural areas
- **Blue** — navbar, primary buttons, active links
- **Red** — danger/delete actions only (not mixed across the UI)

Configuration lives in `config/jazzmin_settings.py` and `static/css/jazzmin-theme.css`.

The admin panel includes:

- Searchable and filterable algorithm management
- Inline management of related resources, comments, and ratings
- Bookmark and favorite relationship inspection
- Profile management
- Branded admin dashboard for demonstration use

## Academic Notes

This project is intentionally structured for an academic software engineering context:

- Multi-app separation of concerns
- Reusable forms, serializers, and class-based views
- Normalized relational design with constraints and indexes
- ORM optimization through `select_related`, `prefetch_related`, and annotations
- REST API support for future mobile or frontend integration
- Clear Bootstrap UI for demonstrations and thesis screenshots

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/sample_users.json fixtures/sample_content.json
python manage.py runserver
```

## License

This repository includes a `LICENSE` file. Use or adapt the project according to that license.
