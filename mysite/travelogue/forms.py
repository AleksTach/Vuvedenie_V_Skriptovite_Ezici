from django import forms

from .models import Destination


class DestinationForm(forms.ModelForm):
    """Form for quickly adding a new destination card."""

    class Meta:
        model = Destination
        fields = [
            "title",
            "location",
            "vibe",
            "highlight",
            "description",
            "image_url",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "What makes this place special?",
                }
            ),
            "highlight": forms.TextInput(
                attrs={"placeholder": "Sunrise at the dunes, street food crawl, etc."}
            ),
            "image_url": forms.URLInput(
                attrs={"placeholder": "https://images.unsplash.com/..."}
            ),
        }