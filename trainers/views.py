from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Trainer, TrainerComment, TrainerRating
from .forms import TrainerCommentForm
from restaurants.models import City, Advertisement
from gym.models import SportType


def trainer_list(request):
    """نمایش لیست تمام مربیان با صفحه‌بندی و فیلتر"""
    trainers_list = Trainer.objects.prefetch_related(
        'phone_numbers', 
        'images', 
        'ratings',
        'city',
        'sport_types'
    ).annotate(
        avg_rating=Avg('ratings__rating'),
        total_ratings=Count('ratings')
    )
    
    # فیلترها
    city_filter = request.GET.get('city')
    rating_filter = request.GET.get('rating')
    sport_types_filter = request.GET.getlist('sport_type')
    search_query = request.GET.get('search', '').strip()
    
    # جستجوی پیشرفته
    if search_query:
        trainers_list = trainers_list.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if city_filter:
        trainers_list = trainers_list.filter(city__name=city_filter)
    
    if rating_filter:
        try:
            min_rating = float(rating_filter)
            trainers_list = trainers_list.filter(avg_rating__gte=min_rating)
        except ValueError:
            pass
    
    if sport_types_filter:
        trainers_list = trainers_list.filter(sport_types__name__in=sport_types_filter).distinct()
    
    # صفحه‌بندی: 9 مربی در هر صفحه
    paginator = Paginator(trainers_list, 9)
    page_number = request.GET.get('page', 1)
    trainers = paginator.get_page(page_number)
    
    # دریافت تبلیغات فعال برای مربیان
    left_ads = Advertisement.objects.filter(section='trainer', position='right', is_active=True).order_by('order')[:3]
    right_ads = Advertisement.objects.filter(section='trainer', position='left', is_active=True).order_by('order')[:3]
    
    # دریافت لیست‌ها برای فیلتر
    cities = City.objects.all()
    # ترتیب نوع ورزش: سایر موارد در آخر
    sport_types_list = list(SportType.objects.all())
    sport_types = sorted(sport_types_list, key=lambda x: (x.name == 'other', x.name))
    
    context = {
        'trainers': trainers,
        'left_ads': left_ads,
        'right_ads': right_ads,
        'cities': cities,
        'sport_types': sport_types,
        'current_city': city_filter,
        'current_rating': rating_filter,
        'current_sport_types': sport_types_filter,
        'search_query': search_query,
    }
    
    return render(request, 'trainers/list.html', context)


def trainer_detail(request, pk):
    """نمایش جزئیات یک مربی"""
    trainer = get_object_or_404(
        Trainer.objects.prefetch_related('phone_numbers', 'images', 'comments', 'ratings'),
        pk=pk
    )
    
    # محاسبه میانگین ریتینگ
    ratings = trainer.ratings.all()
    avg_rating = 0
    if ratings.exists():
        avg_rating = sum(r.rating for r in ratings) / ratings.count()
    
    # نمایش کامنت‌های تایید شده
    comments = trainer.comments.filter(is_approved=True)
    
    # فرم کامنت
    if request.method == 'POST':
        form = TrainerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            
            # ایجاد ریتینگ
            rating_value = int(form.cleaned_data['rating'])
            rating = TrainerRating.objects.create(
                trainer=trainer,
                rating=rating_value
            )
            comment.rating = rating
            comment.trainer = trainer
            comment.save()
            
            messages.success(request, 'نظر و امتیاز شما با موفقیت ثبت شد!')
            return redirect('trainers:detail', pk=trainer.pk)
    else:
        form = TrainerCommentForm()
    
    context = {
        'trainer': trainer,
        'comments': comments,
        'avg_rating': round(avg_rating, 1) if avg_rating > 0 else 0,
        'total_ratings': ratings.count(),
        'form': form,
    }
    
    return render(request, 'trainers/detail.html', context)
