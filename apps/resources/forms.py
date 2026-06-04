"""Forms for resource discovery and bookmarking workflows."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ResourceType


class BootstrapFormMixin:
    """Apply Bootstrap 5 classes to resource forms."""

    def apply_bootstrap_classes(self) -> None:
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} {css_class}".strip()


class ResourceFilterForm(BootstrapFormMixin, forms.Form):
    """Capture resource search and ordering inputs."""

    q = forms.CharField(required=False, max_length=255, label=_("Search"))
    resource_type = forms.ChoiceField(
        required=False,
        choices=[("", _("All Resource Types")), *ResourceType.choices],
        label=_("Resource type"),
    )
    ordering = forms.ChoiceField(
        required=False,
        choices=(
            ("date", _("Latest")),
            ("popularity", _("Popularity")),
            ("title", _("Title")),
        ),
        label=_("Ordering"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()
