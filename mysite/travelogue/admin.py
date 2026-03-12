from django.contrib import admin

from .models import Destination, Experience


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
	list_display = ("title", "location", "vibe", "created_at")
	search_fields = ("title", "location", "vibe")
	prepopulated_fields = {"slug": ("title",)}


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
	list_display = ("title", "destination", "duration")
	list_filter = ("destination",)
	search_fields = ("title", "detail")
