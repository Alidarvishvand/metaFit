from django import template

register = template.Library()


@register.filter
def star_rating(value):
    """تبدیل عدد ریتینگ به ستاره‌ها"""
    if not value:
        return []
    rating = round(float(value))
    stars = []
    for i in range(1, 6):
        if i <= rating:
            stars.append('★')
        else:
            stars.append('☆')
    return stars


