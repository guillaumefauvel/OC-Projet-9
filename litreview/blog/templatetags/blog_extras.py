from django.template import Library
from datetime import datetime, timedelta
from django.utils import timezone


register = Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def add_paranthesis(context, content):
    if content:
        return f'({content})'
    else:
        return ''


@register.simple_tag(takes_context=True)
def time_context(context, time_reference):

    time_difference = timezone.now()-time_reference

    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 4:
        return f'le {time_reference.strftime("%d/%m/%Y à %H:%M")}'
    elif days > 1:
        return f'Il y a {days} jours'
    elif days == 1:
        return 'Hier'
    elif hours > 1:
        return f'Il y a {hours} heures'
    elif minutes > 1:
        return f'Il y a {minutes} minutes'
    else:
        return f'Il y a 1 minute'
