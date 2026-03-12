from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
	"""A curated location travelers can explore and save."""

	title = models.CharField(max_length=80)
	location = models.CharField(max_length=80)
	vibe = models.CharField(max_length=60)
	description = models.TextField()
	highlight = models.CharField(max_length=140)
	image_url = models.URLField()
	slug = models.SlugField(unique=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["title"]

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.title)
			slug = base_slug
			counter = 1
			while Destination.objects.filter(slug=slug).exists():
				slug = f"{base_slug}-{counter}"
				counter += 1
			self.slug = slug
		super().save(*args, **kwargs)


class Experience(models.Model):
	"""Supplementary recommendations tied to a destination."""

	destination = models.ForeignKey(
		Destination,
		related_name="experiences",
		on_delete=models.CASCADE,
	)
	title = models.CharField(max_length=80)
	detail = models.TextField()
	duration = models.CharField(max_length=60)

	class Meta:
		ordering = ["title"]

	def __str__(self):
		return f"{self.title} · {self.destination.title}"
