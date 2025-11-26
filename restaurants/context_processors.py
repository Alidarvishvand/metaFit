from .models import Category


def categories(request):
    """افزودن دسته‌بندی‌ها به context همه صفحات"""
    return {
        'categories': Category.objects.filter(is_active=True).order_by('order')
    }

