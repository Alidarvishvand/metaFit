from django.core.management.base import BaseCommand
from restaurants.models import MealType


class Command(BaseCommand):
    help = 'Create initial meal types'

    def handle(self, *args, **options):
        meal_types = [
            ('breakfast', 'صبحانه'),
            ('lunch', 'ناهار'),
            ('dinner', 'شام'),
            ('snack', 'میان‌وعده'),
            ('all', 'همه'),
        ]
        
        for code, name in meal_types:
            MealType.objects.get_or_create(name=code)
            self.stdout.write(self.style.SUCCESS(f'Meal type "{code}" created'))
        
        self.stdout.write(self.style.SUCCESS('All meal types created successfully'))

