from datetime import datetime
from django.shortcuts import render


def home(request):
    """Landing page showcasing a vibrant hero layout."""
    highlights = [
        "Ultra-fast development with Django",
        "Reusable components and templates",
        "Integrated ORM and admin tooling",
    ]
    context = {
        "highlights": highlights,
        "year": datetime.now().year,
    }
    return render(request, "home.html", context)
