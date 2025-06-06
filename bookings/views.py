from rest_framework import generics, status
from rest_framework.response import Response
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils import timezone
from django.db import transaction


class FitnessClassList(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        # Only show upcoming classes
        return FitnessClass.objects.filter(datetime__gte=timezone.now())


class CreateBooking(generics.CreateAPIView):
    serializer_class = BookingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        fitness_class = serializer.validated_data['fitness_class']

        # Reduce available slots
        fitness_class.available_slots -= 1
        fitness_class.save()

        serializer.save()


class ClientBookings(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email', None)
        if email is not None:
            return Booking.objects.filter(client_email=email).select_related('fitness_class')
        return Booking.objects.none()