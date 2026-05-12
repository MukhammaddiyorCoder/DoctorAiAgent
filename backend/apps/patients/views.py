from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    search_fields = ("full_name", "phone", "email")
    filterset_fields = ("gender",)

    def get_queryset(self):
        return Patient.objects.filter(clinic__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user.clinic)
