from django import template
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime, date

register = template.Library()


@register.filter(name='round_timesince')
def round_timesince(value):
    """
    Rounds the timesince to the largest unit.
    """
    if value:
        now = timezone.now()

        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())

        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())

        return timesince(value, now).split(', ')[0]
    return ''
