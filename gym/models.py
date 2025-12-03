from django.db import models
from restaurants.models import City


class SportType(models.Model):
    SPORT_CHOICES = [
        ('bodybuilding', 'بدنسازی'),
        ('horse_riding', 'سوارکاری'),
        ('swimming', 'شنا'),
        ('football', 'فوتبال'),
        ('volleyball', 'والیبال'),
        ('yoga', 'یوگا'),
        ('crossfit', 'کراس فیت'),
        ('pilates', 'پیلاتس'),
        ('handball', 'هندبال'),
        ('other', 'سایر موارد'),
    ]
    
    name = models.CharField(max_length=20, choices=SPORT_CHOICES, unique=True, verbose_name="نوع ورزش")
    
    class Meta:
        verbose_name = "نوع ورزش"
        verbose_name_plural = "انواع ورزش"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class PriceRange(models.Model):
    PRICE_CHOICES = [
        ('low', 'اقتصادی'),
        ('medium', 'متوسط'),
        ('high', 'گران'),
        ('premium', 'لوکس'),
    ]
    
    name = models.CharField(max_length=20, choices=PRICE_CHOICES, unique=True, verbose_name="محدوده قیمت")
    
    class Meta:
        verbose_name = "محدوده قیمت"
        verbose_name_plural = "محدوده‌های قیمت"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Facility(models.Model):
    FACILITY_CHOICES = [
        ('pool', 'استخر'),
        ('sauna', 'سونا'),
        ('jacuzzi', 'جکوزی'),
        ('parking', 'پارکینگ'),
        ('cafe', 'کافه'),
        ('locker_room', 'رختکن'),
        ('other', 'سایر موارد'),
    ]
    
    name = models.CharField(max_length=20, choices=FACILITY_CHOICES, unique=True, verbose_name="امکانات")
    
    class Meta:
        verbose_name = "امکانات"
        verbose_name_plural = "امکانات"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Gym(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام باشگاه")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='gyms', verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    sport_types = models.ManyToManyField(SportType, related_name='gyms', verbose_name="نوع ورزش", blank=True)
    price_range = models.ForeignKey(PriceRange, on_delete=models.SET_NULL, null=True, blank=True, related_name='gyms', verbose_name="محدوده قیمت")
    facilities = models.ManyToManyField(Facility, related_name='gyms', verbose_name="امکانات", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "باشگاه"
        verbose_name_plural = "باشگاه‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class GymPhoneNumber(models.Model):
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name="باشگاه"
    )
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")

    class Meta:
        verbose_name = "شماره تلفن"
        verbose_name_plural = "شماره‌های تلفن"

    def __str__(self):
        return f"{self.gym.name} - {self.phone}"


class GymImage(models.Model):
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="باشگاه"
    )
    image = models.ImageField(upload_to='gyms/', verbose_name="عکس")
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "عکس باشگاه"
        verbose_name_plural = "عکس‌های باشگاه"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gym.name} - {self.description or 'عکس'}"


class GymRating(models.Model):
    RATING_CHOICES = [
        (1, '1 ستاره'),
        (2, '2 ستاره'),
        (3, '3 ستاره'),
        (4, '4 ستاره'),
        (5, '5 ستاره'),
    ]
    
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name="باشگاه"
    )
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="امتیاز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gym.name} - {self.rating} ستاره"


class GymComment(models.Model):
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="باشگاه"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل", blank=True, null=True)
    comment = models.TextField(verbose_name="نظر")
    rating = models.ForeignKey(
        GymRating,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='comment',
        verbose_name="امتیاز مرتبط"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_approved = models.BooleanField(default=True, verbose_name="تایید شده")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gym.name} - {self.name}"
