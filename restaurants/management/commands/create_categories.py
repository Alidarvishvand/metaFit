from django.core.management.base import BaseCommand
from restaurants.models import Category


class Command(BaseCommand):
    help = 'Create initial categories'

    def handle(self, *args, **options):
        categories = [
            ('gym', 'باشگاه', '💪', 1),
            ('restaurant', 'رستوران', '🍽️', 2),
            ('trainer', 'مربیان', '🏋️', 3),
            ('doctor', 'پزشکان', '👨‍⚕️', 4),
        ]
        
        for code, name, icon, order in categories:
            Category.objects.get_or_create(
                name=code,
                defaults={'icon': icon, 'order': order}
            )
            self.stdout.write(self.style.SUCCESS(f'Category "{code}" created'))
        
        self.stdout.write(self.style.SUCCESS('All categories created successfully'))







