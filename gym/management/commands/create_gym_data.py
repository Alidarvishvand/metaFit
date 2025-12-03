import sys
from django.core.management.base import BaseCommand
from gym.models import SportType, PriceRange, Facility


class Command(BaseCommand):
    help = 'ایجاد داده‌های اولیه برای نوع ورزش، محدوده قیمت و امکانات'

    def handle(self, *args, **options):
        sys.stdout.reconfigure(encoding='utf-8')
        
        # ایجاد انواع ورزش
        sport_types = [
            'bodybuilding',
            'horse_riding',
            'swimming',
            'football',
            'volleyball',
            'yoga',
            'crossfit',
            'pilates',
            'handball',
            'other',
        ]
        
        for sport in sport_types:
            SportType.objects.get_or_create(name=sport)
            self.stdout.write(self.style.SUCCESS(f'✓ نوع ورزش "{sport}" ایجاد شد'))
        
        # ایجاد محدوده‌های قیمت
        price_ranges = [
            'low',
            'medium',
            'high',
            'premium',
        ]
        
        for price in price_ranges:
            PriceRange.objects.get_or_create(name=price)
            self.stdout.write(self.style.SUCCESS(f'✓ محدوده قیمت "{price}" ایجاد شد'))
        
        # ایجاد امکانات
        facilities = [
            'pool',
            'sauna',
            'jacuzzi',
            'parking',
            'cafe',
            'locker_room',
            'other',
        ]
        
        for facility in facilities:
            Facility.objects.get_or_create(name=facility)
            self.stdout.write(self.style.SUCCESS(f'✓ امکانات "{facility}" ایجاد شد'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ تمام داده‌های اولیه با موفقیت ایجاد شدند!'))




