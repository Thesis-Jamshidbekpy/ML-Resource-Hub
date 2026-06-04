"""Forms for algorithm discovery, comments, and ratings."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AlgorithmCategory, Comment, Rating


class BootstrapFormMixin:
    """Apply Bootstrap 5 form classes consistently."""

    def apply_bootstrap_classes(self) -> None:
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} {css_class}".strip()


class AlgorithmFilterForm(BootstrapFormMixin, forms.Form):
    """Capture search, category, and ordering preferences."""

    q = forms.CharField(required=False, label=_("Search"), max_length=255)
    category = forms.ChoiceField(
        required=False,
        choices=[("", _("All Categories")), *AlgorithmCategory.choices],
    )
    ordering = forms.ChoiceField(
        required=False,
        choices=(
            ("name", _("Name")),
            ("popularity", _("Popularity")),
            ("date", _("Latest")),
        ),
        label=_("Ordering"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()


class CommentForm(BootstrapFormMixin, forms.ModelForm):
    """Collect user commentary on algorithm detail pages."""

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": _("Share your insight or experience.")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()


class RatingForm(BootstrapFormMixin, forms.ModelForm):
    """Collect a one-to-five rating for an algorithm."""

    class Meta:
        model = Rating
        fields = ("score",)
        widgets = {
            "score": forms.Select(choices=[(score, f"{score} / 5") for score in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()
