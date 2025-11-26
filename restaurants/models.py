from django.db import models


class Category(models.Model):
    """دسته‌بندی‌های اصلی"""
    CATEGORY_CHOICES = [
        ('gym', 'باشگاه'),
        ('restaurant', 'رستوران'),
        ('trainer', 'مربیان'),
        ('doctor', 'پزشکان'),
    ]
    
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True, verbose_name="نام دسته")
    icon = models.CharField(max_length=10, blank=True, null=True, verbose_name="آیکون")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.get_name_display()


class City(models.Model):
    """31 استان ایران"""
    IRAN_PROVINCES = [
        ('tehran', 'تهران'),
        ('isfahan', 'اصفهان'),
        ('fars', 'فارس'),
        ('khorasan-razavi', 'خراسان رضوی'),
        ('azarbaijan-sharghi', 'آذربایجان شرقی'),
        ('mazandaran', 'مازندران'),
        ('khorasan-shomali', 'خراسان شمالی'),
        ('khorasan-jonubi', 'خراسان جنوبی'),
        ('alborz', 'البرز'),
        ('gilan', 'گیلان'),
        ('kerman', 'کرمان'),
        ('lorestan', 'لرستان'),
        ('azarbaijan-gharbi', 'آذربایجان غربی'),
        ('hamadan', 'همدان'),
        ('kermanshah', 'کرمانشاه'),
        ('yazd', 'یزد'),
        ('ardabil', 'اردبیل'),
        ('bushehr', 'بوشهر'),
        ('zanjan', 'زنجان'),
        ('semnan', 'سمنان'),
        ('qom', 'قم'),
        ('golestan', 'گلستان'),
        ('qazvin', 'قزوین'),
        ('markazi', 'مرکزی'),
        ('chaharmahal-bakhtiari', 'چهارمحال و بختیاری'),
        ('kohgiluyeh-boyer-ahmad', 'کهگیلویه و بویراحمد'),
        ('ilam', 'ایلام'),
        ('kordestan', 'کردستان'),
        ('hormozgan', 'هرمزگان'),
        ('sistan-baluchestan', 'سیستان و بلوچستان'),
        ('west-azarbaijan', 'آذربایجان غربی'),
    ]
    
    name = models.CharField(max_length=50, choices=IRAN_PROVINCES, unique=True, verbose_name="نام استان")
    
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class MealType(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'صبحانه'),
        ('lunch', 'ناهار'),
        ('dinner', 'شام'),
        ('snack', 'میان‌وعده'),
        ('all', 'همه'),
    ]
    
    name = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, unique=True, verbose_name="نوع وعده")
    
    class Meta:
        verbose_name = "نوع وعده"
        verbose_name_plural = "انواع وعده"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Restaurant(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام رستوران")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurants', verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    meal_types = models.ManyToManyField(MealType, blank=True, related_name='restaurants', verbose_name="انواع وعده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "رستوران"
        verbose_name_plural = "رستوران‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name="رستوران"
    )
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")

    class Meta:
        verbose_name = "شماره تلفن"
        verbose_name_plural = "شماره‌های تلفن"

    def __str__(self):
        return f"{self.restaurant.name} - {self.phone}"


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="رستوران"
    )
    image = models.ImageField(upload_to='restaurants/', verbose_name="عکس")
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "عکس رستوران"
        verbose_name_plural = "عکس‌های رستوران"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.restaurant.name} - {self.description or 'عکس'}"


class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 ستاره'),
        (2, '2 ستاره'),
        (3, '3 ستاره'),
        (4, '4 ستاره'),
        (5, '5 ستاره'),
    ]
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name="رستوران"
    )
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="امتیاز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating} ستاره"


class Comment(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="رستوران"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل", blank=True, null=True)
    comment = models.TextField(verbose_name="نظر")
    rating = models.ForeignKey(
        Rating,
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
        return f"{self.restaurant.name} - {self.name}"


class Advertisement(models.Model):
    AD_TYPE_CHOICES = [
        ('image', 'عکس'),
        ('gif', 'گیف'),
        ('video', 'ویدیو'),
    ]
    
    POSITION_CHOICES = [
        ('left', 'سمت چپ'),
        ('right', 'سمت راست'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES, default='image', verbose_name="نوع تبلیغ")
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True, verbose_name="عکس")
    gif_file = models.FileField(upload_to='advertisements/gifs/', blank=True, null=True, verbose_name="فایل گیف")
    video_file = models.FileField(upload_to='advertisements/videos/', blank=True, null=True, verbose_name="فایل ویدیو")
    video_url = models.URLField(blank=True, null=True, verbose_name="لینک ویدیو (اختیاری)")
    link = models.URLField(blank=True, null=True, verbose_name="لینک (اختیاری)")
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, verbose_name="موقعیت")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"
        ordering = ['position', 'order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_position_display()}"
