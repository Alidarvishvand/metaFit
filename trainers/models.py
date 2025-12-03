from django.db import models
from django.core.validators import FileExtensionValidator
from restaurants.models import City
from gym.models import SportType


class Trainer(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام مربی")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainers', verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    resume = models.FileField(
        upload_to='trainer_resumes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
        verbose_name="رزومه (PDF)"
    )
    sport_types = models.ManyToManyField(SportType, related_name='trainers', verbose_name="نوع ورزش", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "مربی"
        verbose_name_plural = "مربیان"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TrainerPhoneNumber(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name="مربی"
    )
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")

    class Meta:
        verbose_name = "شماره تلفن"
        verbose_name_plural = "شماره‌های تلفن"

    def __str__(self):
        return f"{self.trainer.name} - {self.phone}"


class TrainerImage(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="مربی"
    )
    image = models.ImageField(upload_to='trainers/', verbose_name="عکس")
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "عکس مربی"
        verbose_name_plural = "عکس‌های مربی"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trainer.name} - {self.description or 'عکس'}"


class TrainerRating(models.Model):
    RATING_CHOICES = [
        (1, '1 ستاره'),
        (2, '2 ستاره'),
        (3, '3 ستاره'),
        (4, '4 ستاره'),
        (5, '5 ستاره'),
    ]
    
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name="مربی"
    )
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="امتیاز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trainer.name} - {self.rating} ستاره"


class TrainerComment(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="مربی"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل", blank=True, null=True)
    comment = models.TextField(verbose_name="نظر")
    rating = models.ForeignKey(
        TrainerRating,
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
        return f"{self.trainer.name} - {self.name}"
