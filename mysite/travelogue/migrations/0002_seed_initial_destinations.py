from django.db import migrations
from django.utils.text import slugify


def seed_destinations(apps, schema_editor):
    Destination = apps.get_model("travelogue", "Destination")
    Experience = apps.get_model("travelogue", "Experience")

    dataset = [
        {
            "title": "Atlas Sunrise Camp",
            "location": "Morocco",
            "vibe": "desert modernism",
            "highlight": "Daybreak over the Erg Chebbi dunes",
            "description": "A minimalist camp outside Merzouga where clay walls keep the tents cool and endless dunes sit ten minutes away by foot.",
            "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
            "experiences": [
                {
                    "title": "Dune climb",
                    "detail": "Headlamp hike at 4:30 a.m. to claim the tallest ridge before the sun crests.",
                    "duration": "2 hours",
                },
                {
                    "title": "Caravan supper",
                    "detail": "Shared tagine dinner under a field of lanterns with local Gnawa musicians.",
                    "duration": "Evening",
                },
            ],
        },
        {
            "title": "Lisbon Coast Studio",
            "location": "Portugal",
            "vibe": "atlantic creative hub",
            "highlight": "Tram 28 to rooftop sketch sessions",
            "description": "A converted ceramics warehouse in Graça with high ceilings, salty breezes, and a rotating residency of illustrators.",
            "image_url": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade",
            "experiences": [
                {
                    "title": "Azulejo workshop",
                    "detail": "Two-hour glaze class with a fourth-generation tile artist.",
                    "duration": "Morning",
                },
                {
                    "title": "Miradouro picnic",
                    "detail": "Forage pastel de nata, canned fish, and vinho verde on the hilltop garden.",
                    "duration": "Sunset",
                },
                {
                    "title": "LX Factory night ride",
                    "detail": "Cycle along the docks to see the light installations and grab midnight espresso.",
                    "duration": "Late night",
                },
            ],
        },
        {
            "title": "Kyoto Slow Bloom",
            "location": "Japan",
            "vibe": "quiet craft immersion",
            "highlight": "Cycling Arashiyama before the crowds arrive",
            "description": "Townhouse stay with tatami studios devoted to indigo dyeing, tea whisk carving, and garden journaling.",
            "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            "experiences": [
                {
                    "title": "Tea atelier",
                    "detail": "Learn matcha etiquette from a Urasenke master inside a six-mat chashitsu.",
                    "duration": "3 hours",
                },
                {
                    "title": "Indigo lab",
                    "detail": "Dip scarves in natural vats overlooking the koi pond.",
                    "duration": "Afternoon",
                },
            ],
        },
    ]

    for entry in dataset:
        destination = Destination.objects.create(
            title=entry["title"],
            location=entry["location"],
            vibe=entry["vibe"],
            highlight=entry["highlight"],
            description=entry["description"],
            image_url=entry["image_url"],
            slug=slugify(entry["title"]),
        )
        Experience.objects.bulk_create(
            [
                Experience(
                    destination=destination,
                    title=exp["title"],
                    detail=exp["detail"],
                    duration=exp["duration"],
                )
                for exp in entry["experiences"]
            ]
        )


def reset_destinations(apps, schema_editor):
    Destination = apps.get_model("travelogue", "Destination")
    Destination.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("travelogue", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_destinations, reset_destinations),
    ]
