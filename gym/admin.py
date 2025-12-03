from django.contrib import admin
from .models import Gym, GymPhoneNumber, GymImage, GymComment, GymRating, SportType, PriceRange, Facility


class GymPhoneNumberInline(admin.TabularInline):
    model = GymPhoneNumber
    extra = 1
    verbose_name = "شماره تلفن"
    verbose_name_plural = "شماره‌های تلفن"


class GymImageInline(admin.TabularInline):
    model = GymImage
    extra = 1
    verbose_name = "عکس"
    verbose_name_plural = "عکس‌های باشگاه"


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'price_range', 'created_at']
    list_filter = ['city', 'price_range', 'sport_types', 'facilities', 'created_at']
    search_fields = ['name', 'address', 'description']
    inlines = [GymPhoneNumberInline, GymImageInline]
    filter_horizontal = ['sport_types', 'facilities']
    fields = ['name', 'city', 'address', 'description', 'sport_types', 'price_range', 'facilities']
    verbose_name = "باشگاه"
    verbose_name_plural = "باشگاه‌ها"


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ['get_name_display']
    verbose_name = "نوع ورزش"
    verbose_name_plural = "انواع ورزش"


@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    list_display = ['get_name_display']
    verbose_name = "محدوده قیمت"
    verbose_name_plural = "محدوده‌های قیمت"


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['get_name_display']
    verbose_name = "امکانات"
    verbose_name_plural = "امکانات"


@admin.register(GymComment)
class GymCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'gym', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'comment', 'gym__name']
    verbose_name = "نظر"
    verbose_name_plural = "نظرات"


@admin.register(GymRating)
class GymRatingAdmin(admin.ModelAdmin):
    list_display = ['gym', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['gym__name']
    verbose_name = "امتیاز"
    verbose_name_plural = "امتیازها"
