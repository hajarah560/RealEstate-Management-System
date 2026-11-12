# Django Admin setup for the properties app.

# Technical: the admin site object that models are registered with.
from django.contrib import admin

from .models import Land, Building

# Plain English: this makes Land and Buildings show up in the built-in Django Admin site
# (/admin/). Technical: plain register() calls give stock admin pages; deliberately not customised.
admin.site.register(Land)
admin.site.register(Building)
