from django.contrib import admin
from .models import Restaurant, PhoneNumber, RestaurantImage, Comment, Rating, Advertisement, City, MealType, Category


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1
    verbose_name = "شماره تلفن"
    verbose_name_plural = "شماره‌های تلفن"


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1
    verbose_name = "عکس"
    verbose_name_plural = "عکس‌های رستوران"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    verbose_name = "دسته‌بندی"
    verbose_name_plural = "دسته‌بندی‌ها"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    verbose_name = "شهر"
    verbose_name_plural = "شهرها"


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    verbose_name = "نوع وعده"
    verbose_name_plural = "انواع وعده"


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'created_at']
    list_filter = ['city', 'meal_types', 'created_at']
    search_fields = ['name', 'address', 'description']
    filter_horizontal = ['meal_types']
    fields = ['name', 'city', 'address', 'description', 'meal_types']
    inlines = [PhoneNumberInline, RestaurantImageInline]
    verbose_name = "رستوران"
    verbose_name_plural = "رستوران‌ها"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'comment', 'restaurant__name']
    verbose_name = "نظر"
    verbose_name_plural = "نظرات"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['restaurant__name']
    verbose_name = "امتیاز"
    verbose_name_plural = "امتیازها"


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'ad_type', 'position', 'order', 'is_active', 'created_at']
    list_filter = ['ad_type', 'position', 'is_active', 'created_at']
    search_fields = ['title']
    fields = ['title', 'ad_type', 'position', 'order', 'is_active', 'link', 'image', 'gif_file', 'video_file', 'video_url']
    verbose_name = "تبلیغ"
    verbose_name_plural = "تبلیغات"
