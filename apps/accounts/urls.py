"""URL routes for authentication and profile management."""

from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    ProfileUpdateView,
    RegisterView,
    UserUpdateView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/update/", UserUpdateView.as_view(), name="profile_update"),
]
