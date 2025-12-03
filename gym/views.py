from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Gym, GymComment, GymRating, SportType, PriceRange, Facility
from .forms import GymCommentForm
from restaurants.models import City, Advertisement


def gym_list(request):
    """نمایش لیست تمام باشگاه‌ها با صفحه‌بندی و فیلتر"""
    gyms_list = Gym.objects.prefetch_related(
        'phone_numbers', 
        'images', 
        'ratings',
        'city',
        'sport_types',
        'facilities'
    ).annotate(
        avg_rating=Avg('ratings__rating'),
        total_ratings=Count('ratings')
    )
    
    # فیلترها
    city_filter = request.GET.get('city')
    rating_filter = request.GET.get('rating')
    sport_types_filter = request.GET.getlist('sport_type')
    price_range_filter = request.GET.get('price_range')
    facilities_filter = request.GET.getlist('facility')
    search_query = request.GET.get('search', '').strip()
    
    # جستجوی پیشرفته
    if search_query:
        from django.db.models import Q
        gyms_list = gyms_list.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if city_filter:
        gyms_list = gyms_list.filter(city__name=city_filter)
    
    if rating_filter:
        try:
            min_rating = float(rating_filter)
            gyms_list = gyms_list.filter(avg_rating__gte=min_rating)
        except ValueError:
            pass
    
    if sport_types_filter:
        gyms_list = gyms_list.filter(sport_types__name__in=sport_types_filter).distinct()
    
    if price_range_filter:
        gyms_list = gyms_list.filter(price_range__name=price_range_filter)
    
    if facilities_filter:
        gyms_list = gyms_list.filter(facilities__name__in=facilities_filter).distinct()
    
    # صفحه‌بندی: 9 باشگاه در هر صفحه
    paginator = Paginator(gyms_list, 9)
    page_number = request.GET.get('page', 1)
    gyms = paginator.get_page(page_number)
    
    # دریافت تبلیغات فعال برای باشگاه
    left_ads = Advertisement.objects.filter(section='gym', position='right', is_active=True).order_by('order')[:3]
    right_ads = Advertisement.objects.filter(section='gym', position='left', is_active=True).order_by('order')[:3]
    
    # دریافت لیست‌ها برای فیلتر
    cities = City.objects.all()
    # ترتیب نوع ورزش: سایر موارد در آخر
    sport_types_list = list(SportType.objects.all())
    sport_types = sorted(sport_types_list, key=lambda x: (x.name == 'other', x.name))
    price_ranges = PriceRange.objects.all()
    # ترتیب امکانات: سایر موارد در آخر
    facilities_list = list(Facility.objects.all())
    facilities = sorted(facilities_list, key=lambda x: (x.name == 'other', x.name))
    
    context = {
        'gyms': gyms,
        'left_ads': left_ads,
        'right_ads': right_ads,
        'cities': cities,
        'sport_types': sport_types,
        'price_ranges': price_ranges,
        'facilities': facilities,
        'current_city': city_filter,
        'current_rating': rating_filter,
        'current_sport_types': sport_types_filter,
        'current_price_range': price_range_filter,
        'current_facilities': facilities_filter,
        'search_query': search_query,
    }
    
    return render(request, 'gym/list.html', context)


def gym_detail(request, pk):
    """نمایش جزئیات یک باشگاه"""
    gym = get_object_or_404(
        Gym.objects.prefetch_related('phone_numbers', 'images', 'comments', 'ratings'),
        pk=pk
    )
    
    # محاسبه میانگین ریتینگ
    ratings = gym.ratings.all()
    avg_rating = 0
    if ratings.exists():
        avg_rating = sum(r.rating for r in ratings) / ratings.count()
    
    # نمایش کامنت‌های تایید شده
    comments = gym.comments.filter(is_approved=True)
    
    # فرم کامنت
    if request.method == 'POST':
        form = GymCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.gym = gym
            
            # ایجاد ریتینگ
            rating_value = int(form.cleaned_data['rating'])
            rating = GymRating.objects.create(
                gym=gym,
                rating=rating_value
            )
            comment.rating = rating
            comment.gym = gym
            comment.save()
            
            messages.success(request, 'نظر و امتیاز شما با موفقیت ثبت شد!')
            return redirect('gym:detail', pk=gym.pk)
    else:
        form = GymCommentForm()
    
    context = {
        'gym': gym,
        'comments': comments,
        'avg_rating': round(avg_rating, 1) if avg_rating > 0 else 0,
        'total_ratings': ratings.count(),
        'form': form,
    }
    
    return render(request, 'gym/detail.html', context)
