from django.urls import path

from .views import (
    PublicBookingView,
    PublicClinicDetailView,
    PublicClinicServicesView,
)

urlpatterns = [
    path(
        "clinic/<slug:slug>/",
        PublicClinicDetailView.as_view(),
        name="public-clinic",
    ),
    path(
        "clinic/<slug:slug>/services/",
        PublicClinicServicesView.as_view(),
        name="public-clinic-services",
    ),
    path(
        "clinic/<slug:slug>/book/",
        PublicBookingView.as_view(),
        name="public-clinic-book",
    ),
]
