from django.core.management.base import BaseCommand
from bookings.models import FitnessClass
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with sample fitness classes'

    def handle(self, *args, **options):
        classes = [
            {
                'name': 'Yoga',
                'datetime': timezone.now() + timezone.timedelta(days=1),
                'instructor': 'Alice Smith',
                'max_capacity': 15,
                'available_slots': 15
            },
            {
                'name': 'Zumba',
                'datetime': timezone.now() + timezone.timedelta(days=2),
                'instructor': 'Bob Johnson',
                'max_capacity': 20,
                'available_slots': 20
            },
            {
                'name': 'HIIT',
                'datetime': timezone.now() + timezone.timedelta(days=3),
                'instructor': 'Charlie Brown',
                'max_capacity': 10,
                'available_slots': 10
            }
        ]

        for class_data in classes:
            FitnessClass.objects.create(**class_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded fitness classes'))