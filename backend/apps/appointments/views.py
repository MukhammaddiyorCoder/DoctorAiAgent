from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    filterset_fields = ("status", "service", "patient")
    search_fields = ("patient__full_name", "patient__phone", "note")
    ordering_fields = ("starts_at", "created_at")

    def get_queryset(self):
        qs = Appointment.objects.filter(
            clinic__owner=self.request.user
        ).select_related("patient", "service")

        # Optional range filtering: ?from=ISO&to=ISO
        start = self.request.query_params.get("from")
        end = self.request.query_params.get("to")
        if start:
            qs = qs.filter(starts_at__gte=start)
        if end:
            qs = qs.filter(starts_at__lte=end)
        return qs

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        now = timezone.now()
        today = now.date()
        qs = Appointment.objects.filter(clinic__owner=request.user)
        data = {
            "total": qs.count(),
            "today": qs.filter(starts_at__date=today).count(),
            "upcoming": qs.filter(starts_at__gte=now).count(),
            "by_status": dict(
                qs.values_list("status").annotate(c=Count("id")).values_list("status", "c")
            ),
            "ai_booked": qs.filter(source=Appointment.Source.AI).count(),
        }
        return Response(data)

    @action(detail=False, methods=["get"], url_path="trend")
    def trend(self, request):
        """
        Return daily appointment counts for the last 14 days. Shape:
        [{"date": "YYYY-MM-DD", "count": N, "ai": N}, ...]
        """
        from datetime import timedelta

        from django.db.models.functions import TruncDate

        days = int(request.query_params.get("days", 14))
        days = max(1, min(days, 90))
        since = timezone.now() - timedelta(days=days)

        rows = (
            Appointment.objects.filter(
                clinic__owner=request.user, starts_at__gte=since
            )
            .annotate(day=TruncDate("starts_at"))
            .values("day")
            .annotate(
                count=Count("id"),
                ai=Count("id", filter=Q(source=Appointment.Source.AI)),
            )
            .order_by("day")
        )
        return Response(
            [
                {
                    "date": r["day"].isoformat(),
                    "count": r["count"],
                    "ai": r["ai"],
                }
                for r in rows
            ]
        )
