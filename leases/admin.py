# Django Admin setup for the leases app.

# Technical: the admin site object that models are registered with.
from django.contrib import admin

from .models import Lease

# Plain English: this makes Leases show up in the built-in Django Admin site (/admin/).
# Technical: a plain register() gives stock admin pages; deliberately not customised.
admin.site.register(Lease)
