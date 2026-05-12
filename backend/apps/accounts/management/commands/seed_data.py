from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.billing.models import Plan, Subscription
from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service

User = get_user_model()

DEMO_EMAIL = "demo@doctor.com"
DEMO_PASSWORD = "demo1234"


class Command(BaseCommand):
    help = "Seed the database with demo data (demo user, clinic, services, patients)."

    def handle(self, *args, **options):
        # ---- Plans ----
        plans_data = [
            {
                "tier": Plan.Tier.FREE,
                "name": "Free",
                "price_monthly": 0,
                "max_appointments_per_month": 50,
                "max_ai_messages_per_month": 100,
                "features": ["1 clinic", "Basic AI", "Public booking"],
            },
            {
                "tier": Plan.Tier.PRO,
                "name": "Pro",
                "price_monthly": 29,
                "max_appointments_per_month": 1000,
                "max_ai_messages_per_month": 5000,
                "features": ["Advanced AI", "Priority support", "Analytics"],
            },
            {
                "tier": Plan.Tier.BUSINESS,
                "name": "Business",
                "price_monthly": 99,
                "max_appointments_per_month": 10000,
                "max_ai_messages_per_month": 50000,
                "features": ["Custom AI prompts", "White-label widget", "SLA"],
            },
        ]
        for data in plans_data:
            Plan.objects.update_or_create(tier=data["tier"], defaults=data)
        self.stdout.write(self.style.SUCCESS("Plans created."))

        # ---- Demo user + clinic ----
        user, created = User.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={
                "full_name": "Dr. Karimov",
                "phone": "+998901234567",
                "role": User.Role.OWNER,
                "is_active": True,
            },
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()

        clinic, _ = Clinic.objects.get_or_create(
            owner=user,
            defaults={
                "name": "Dr. Karimov Clinic",
                "phone": "+998712000000",
                "email": "info@karimov-clinic.uz",
                "address": "Tashkent, Amir Temur ko'chasi 1",
                "description": "Oilaviy tibbiyot va diagnostika markazi.",
            },
        )

        # Ensure subscription
        pro = Plan.objects.get(tier=Plan.Tier.PRO)
        Subscription.objects.update_or_create(
            clinic=clinic,
            defaults={
                "plan": pro,
                "status": Subscription.Status.ACTIVE,
                "current_period_start": timezone.now(),
                "current_period_end": timezone.now() + timedelta(days=30),
            },
        )

        # ---- Services ----
        services_seed = [
            ("Konsultatsiya", 30, 150000),
            ("UZI tekshiruv", 45, 250000),
            ("Qon tahlili", 15, 80000),
            ("Kardiologiya konsultatsiyasi", 60, 350000),
        ]
        for name, duration, price in services_seed:
            Service.objects.get_or_create(
                clinic=clinic,
                name=name,
                defaults={
                    "duration_minutes": duration,
                    "price": price,
                    "currency": "UZS",
                },
            )

        # ---- Patients ----
        patients_seed = [
            ("Alisher Usmonov", "+998901111111"),
            ("Gulnora Tursunova", "+998902222222"),
            ("Bobur Rahimov", "+998903333333"),
        ]
        for full_name, phone in patients_seed:
            Patient.objects.get_or_create(
                clinic=clinic,
                phone=phone,
                defaults={"full_name": full_name},
            )

        # ---- A couple of upcoming appointments ----
        consult = Service.objects.filter(clinic=clinic).first()
        patient = Patient.objects.filter(clinic=clinic).first()
        if consult and patient and not Appointment.objects.filter(clinic=clinic).exists():
            base = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
            Appointment.objects.create(
                clinic=clinic,
                patient=patient,
                service=consult,
                starts_at=base,
                ends_at=base + timedelta(minutes=consult.duration_minutes),
                status=Appointment.Status.CONFIRMED,
                source=Appointment.Source.MANUAL,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed done. Login: {DEMO_EMAIL} / {DEMO_PASSWORD}"
            )
        )
