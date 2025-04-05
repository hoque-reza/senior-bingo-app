# card_gen/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    """Returns the item at the given index from the list."""
    try:
        return list[index]
    except (IndexError, TypeError):
        return None