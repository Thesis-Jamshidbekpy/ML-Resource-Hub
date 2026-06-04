"""Forms used by the landing page and unified search experience."""

from django import forms


class GlobalSearchForm(forms.Form):
    """Capture top-level free-text queries from the shared navbar."""

    q = forms.CharField(max_length=255, required=False, label="Search")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Search algorithms or resources...",
            }
        )
