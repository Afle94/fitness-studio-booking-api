from django.db import models
from django.core.validators import MinValueValidator, EmailValidator

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    max_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.datetime}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(validators=[EmailValidator()])
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class}"