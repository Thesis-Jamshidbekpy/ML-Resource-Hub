"""Top-level URL routes for the ML Resource Hub platform."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("apps.dashboard.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("algorithms/", include("apps.algorithms.urls")),
    path("resources/", include("apps.resources.urls")),
    path("api/", include("apps.algorithms.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
