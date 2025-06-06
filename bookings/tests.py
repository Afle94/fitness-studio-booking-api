from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import FitnessClass


class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test class
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime=timezone.now() + timezone.timedelta(days=1),
            instructor="John Doe",
            max_capacity=10,
            available_slots=10
        )

        self.booking_data = {
            'fitness_class': self.fitness_class.id,
            'client_name': 'Test User',
            'client_email': 'test@example.com'
        }

    def test_get_classes(self):
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        response = self.client.post('/book/', self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check available slots decreased
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 9)

    def test_overbooking(self):
        # Book all available slots
        self.fitness_class.available_slots = 1
        self.fitness_class.save()

        # First booking should succeed
        response = self.client.post('/book/', self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Second booking should fail
        response = self.client.post('/book/', {
            'fitness_class': self.fitness_class.id,
            'client_name': 'Another User',
            'client_email': 'another@example.com'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_client_bookings(self):
        # Create booking first
        self.client.post('/book/', self.booking_data, format='json')

        # Get bookings
        response = self.client.get('/bookings/?email=test@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)