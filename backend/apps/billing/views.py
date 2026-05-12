from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Plan.objects.all()


class MySubscriptionView(APIView):
    def get(self, request):
        clinic = request.user.clinic
        sub = Subscription.objects.filter(clinic=clinic).select_related("plan").first()
        if sub is None:
            return Response({"detail": "No active subscription."}, status=404)
        return Response(SubscriptionSerializer(sub).data)
