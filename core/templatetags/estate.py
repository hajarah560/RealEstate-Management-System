# Custom template helpers for the whole project.
#
# Plain English: a template filter is a small function you can use inside an HTML
# template with a pipe, for example {{ payment.amount|money }}. Technical: Django
# finds this file because it lives in a templatetags/ folder of an installed app;
# a template switches it on with {% load estate %}.

# Plain English: Django's tool for registering template helpers.
from django import template

# Technical: Django looks for a variable named "register" in this file.
register = template.Library()


# Plain English: marks the function below as a filter named "money".
# Technical: used in templates as {{ x|money }} (dashboard totals, payments, prices).
@register.filter
def money(value):
    """Show a number as UGX with thousands separators."""
    # Plain English: if the value is missing or is not a number, show UGX 0 instead of
    # crashing the whole page. Technical: float(None or 0) is fine, but float("abc")
    # raises ValueError and float of a list raises TypeError, so we catch both.
    try:
        return f"UGX {float(value or 0):,.0f}"
    except (TypeError, ValueError):
        return "UGX 0"
