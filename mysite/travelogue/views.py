from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DestinationForm
from .models import Destination


def destination_list(request):
	destinations = (
		Destination.objects.prefetch_related("experiences")
		.annotate(experience_count=Count("experiences"))
		.order_by("title")
	)

	form = DestinationForm()
	if request.method == "POST":
		form = DestinationForm(request.POST)
		if form.is_valid():
			destination = form.save()
			messages.success(
				request,
				f"Added {destination.title} to the Wanderlist.",
			)
			return redirect("travelogue:destinations")

	hero = destinations.first()
	context = {
		"destinations": destinations,
		"hero": hero,
		"form": form,
	}
	return render(request, "travelogue/destination_list.html", context)


def destination_detail(request, slug):
	destination = get_object_or_404(
		Destination.objects.prefetch_related("experiences"), slug=slug
	)
	return render(
		request,
		"travelogue/destination_detail.html",
		{"destination": destination},
	)
