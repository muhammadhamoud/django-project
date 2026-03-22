from django import template

register = template.Library()

@register.filter
def is_odd(index):
    return index % 2 != 0