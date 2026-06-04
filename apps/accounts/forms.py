"""Forms supporting authentication and user profile management."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class BootstrapFormMixin:
    """Apply Bootstrap styling consistently across form widgets."""

    def apply_bootstrap_classes(self) -> None:
        for field in self.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} {css_class}".strip()


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    """Collect standard registration data using Django's auth system."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    """Style Django's built-in authentication form for Bootstrap templates."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    """Update first-class identity fields stored on the user table."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    """Update extended profile metadata for the graduation project portal."""

    class Meta:
        model = Profile
        fields = ("bio", "avatar", "institution", "academic_interest")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()
