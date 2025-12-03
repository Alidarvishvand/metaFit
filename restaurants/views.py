from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Restaurant, Comment, Rating, Advertisement, City, Category
from .forms import CommentForm


def restaurant_list(request):
    """نمایش لیست تمام رستوران‌ها با صفحه‌بندی و فیلتر"""
    restaurants_list = Restaurant.objects.prefetch_related(
        'phone_numbers', 
        'images', 
        'ratings',
        'city',
        'meal_types'
    ).annotate(
        avg_rating=Avg('ratings__rating'),
        total_ratings=Count('ratings')
    )
    
    # فیلترها
    city_filter = request.GET.get('city')
    rating_filter = request.GET.get('rating')
    meal_type_filters = request.GET.getlist('meal_type')  # چند انتخابی
    search_query = request.GET.get('search', '').strip()
    
    # جستجوی پیشرفته
    if search_query:
        from django.db.models import Q
        restaurants_list = restaurants_list.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if city_filter:
        restaurants_list = restaurants_list.filter(city__name=city_filter)
    
    if rating_filter:
        try:
            min_rating = float(rating_filter)
            restaurants_list = restaurants_list.filter(avg_rating__gte=min_rating)
        except ValueError:
            pass
    
    if meal_type_filters:
        # فیلتر بر اساس چند نوع وعده
        restaurants_list = restaurants_list.filter(meal_types__name__in=meal_type_filters).distinct()
    
    # صفحه‌بندی: 9 رستوران در هر صفحه
    paginator = Paginator(restaurants_list, 9)
    page_number = request.GET.get('page', 1)
    restaurants = paginator.get_page(page_number)
    
    # دریافت تبلیغات فعال برای رستوران - اصلاح موقعیت
    # در RTL: left در template = right در دیتابیس
    left_ads = Advertisement.objects.filter(section='restaurant', position='right', is_active=True).order_by('order')[:3]
    right_ads = Advertisement.objects.filter(section='restaurant', position='left', is_active=True).order_by('order')[:3]
    
    # دریافت لیست شهرها برای فیلتر
    cities = City.objects.all()
    
    # دریافت دسته‌بندی‌های فعال
    categories = Category.objects.filter(is_active=True).order_by('order')
    
    context = {
        'restaurants': restaurants,
        'left_ads': left_ads,
        'right_ads': right_ads,
        'cities': cities,
        'categories': categories,
        'current_city': city_filter,
        'current_rating': rating_filter,
        'current_meal_types': meal_type_filters,
        'search_query': search_query,
    }
    
    return render(request, 'restaurants/list.html', context)


def restaurant_detail(request, pk):
    """نمایش جزئیات یک رستوران"""
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('phone_numbers', 'images', 'comments', 'ratings'),
        pk=pk
    )
    
    # محاسبه میانگین ریتینگ
    ratings = restaurant.ratings.all()
    avg_rating = 0
    if ratings.exists():
        avg_rating = sum(r.rating for r in ratings) / ratings.count()
    
    # نمایش کامنت‌های تایید شده
    comments = restaurant.comments.filter(is_approved=True)
    
    # فرم کامنت
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            
            # ایجاد ریتینگ
            rating_value = int(form.cleaned_data['rating'])
            rating = Rating.objects.create(
                restaurant=restaurant,
                rating=rating_value
            )
            comment.rating = rating
            comment.save()
            
            messages.success(request, 'نظر و امتیاز شما با موفقیت ثبت شد!')
            return redirect('restaurants:detail', pk=restaurant.pk)
    else:
        form = CommentForm()
    
    # دریافت دسته‌بندی‌های فعال
    categories = Category.objects.filter(is_active=True).order_by('order')
    
    context = {
        'restaurant': restaurant,
        'comments': comments,
        'avg_rating': round(avg_rating, 1) if avg_rating > 0 else 0,
        'total_ratings': ratings.count(),
        'form': form,
        'categories': categories,
    }
    
    return render(request, 'restaurants/detail.html', context)
