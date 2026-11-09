from django import template

register = template.Library()


@register.filter
def money(value):
    """Show a number as UGX with thousands separators."""
    try:
        return f"UGX {float(value or 0):,.0f}"
    except (TypeError, ValueError):
        return "UGX 0"
