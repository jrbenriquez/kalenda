from dateutil.parser import parse
from django import template

register = template.Library()


@register.filter
def stringtodate(value):
    passed_date = parse(value)
    return passed_date.strftime('%B %d, %Y %-I:%M %p')
