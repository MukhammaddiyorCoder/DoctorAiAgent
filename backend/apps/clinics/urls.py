from django.urls import path

from .views import MyClinicView

urlpatterns = [
    path("", MyClinicView.as_view(), name="clinic-detail"),
]
