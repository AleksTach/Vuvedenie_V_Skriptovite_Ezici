from django.urls import path

from . import views

app_name = "travelogue"

urlpatterns = [
    path("", views.destination_list, name="destinations"),
    path("place/<slug:slug>/", views.destination_detail, name="destination_detail"),
]
