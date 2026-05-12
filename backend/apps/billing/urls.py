from django.urls import path

from .views import MySubscriptionView, PlanListView

urlpatterns = [
    path("plans/", PlanListView.as_view(), name="plans"),
    path("subscription/", MySubscriptionView.as_view(), name="my-subscription"),
]
