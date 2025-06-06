from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'instructor', 'max_capacity', 'available_slots']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booking_time']
        extra_kwargs = {'fitness_class': {'required': True}}

    def validate(self, data):
        fitness_class = data['fitness_class']

        # Check if class is in the future
        if fitness_class.datetime < timezone.now():
            raise serializers.ValidationError("Cannot book a class that has already occurred")

        # Check available slots
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots for this class")

        return data