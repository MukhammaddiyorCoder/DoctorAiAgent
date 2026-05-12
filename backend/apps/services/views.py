from rest_framework import viewsets

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    search_fields = ("name", "description")
    filterset_fields = ("is_active",)

    def get_queryset(self):
        return Service.objects.filter(clinic__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user.clinic)
