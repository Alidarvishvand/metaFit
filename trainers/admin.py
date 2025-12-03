from django.contrib import admin
from .models import Trainer, TrainerPhoneNumber, TrainerImage, TrainerComment, TrainerRating


class TrainerPhoneNumberInline(admin.TabularInline):
    model = TrainerPhoneNumber
    extra = 1
    verbose_name = "شماره تلفن"
    verbose_name_plural = "شماره‌های تلفن"


class TrainerImageInline(admin.TabularInline):
    model = TrainerImage
    extra = 1
    verbose_name = "عکس"
    verbose_name_plural = "عکس‌های مربی"


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'created_at']
    list_filter = ['city', 'sport_types', 'created_at']
    search_fields = ['name', 'address', 'description']
    inlines = [TrainerPhoneNumberInline, TrainerImageInline]
    filter_horizontal = ['sport_types']
    fields = ['name', 'city', 'address', 'description', 'resume', 'sport_types']
    verbose_name = "مربی"
    verbose_name_plural = "مربیان"


@admin.register(TrainerComment)
class TrainerCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'trainer', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'comment', 'trainer__name']
    verbose_name = "نظر"
    verbose_name_plural = "نظرات"


@admin.register(TrainerRating)
class TrainerRatingAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['trainer__name']
    verbose_name = "امتیاز"
    verbose_name_plural = "امتیازها"
