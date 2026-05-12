from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.models import Appointment
from apps.appointments.serializers import PublicAppointmentCreateSerializer
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer

from .models import Clinic
from .serializers import ClinicSerializer, PublicClinicSerializer


class MyClinicView(generics.RetrieveUpdateAPIView):
    """GET / PUT for the authenticated owner's clinic."""

    serializer_class = ClinicSerializer

    def get_object(self):
        return get_object_or_404(Clinic, owner=self.request.user)


class PublicClinicDetailView(generics.RetrieveAPIView):
    """Public view of a clinic by slug."""

    serializer_class = PublicClinicSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = "slug"
    queryset = Clinic.objects.all()


class PublicClinicServicesView(generics.ListAPIView):
    """Public listing of active services for a clinic."""

    serializer_class = ServiceSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Service.objects.filter(
            clinic__slug=self.kwargs["slug"], is_active=True
        )


class PublicBookingView(APIView):
    """Create an appointment without authentication (public booking)."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, slug: str):
        clinic = get_object_or_404(Clinic, slug=slug)
        serializer = PublicAppointmentCreateSerializer(
            data=request.data, context={"clinic": clinic}
        )
        serializer.is_valid(raise_exception=True)
        appointment: Appointment = serializer.save()
        return Response(
            {
                "id": appointment.id,
                "status": appointment.status,
                "starts_at": appointment.starts_at,
                "ends_at": appointment.ends_at,
            },
            status=status.HTTP_201_CREATED,
        )
