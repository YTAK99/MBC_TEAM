from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def relative_time(value):
    if not value:
        return ""

    now = timezone.now()
    diff = now - value

    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "방금 전"

    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}분 전"

    hours = minutes // 60
    if hours < 24:
        return f"{hours}시간 전"

    days = hours // 24
    if days < 30:
        return f"{days}일 전"

    months = days // 30
    if months < 12:
        return f"{months}개월 전"

    years = days // 365
    return f"{years}년 전"