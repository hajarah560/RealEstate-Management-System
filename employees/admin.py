# Django Admin setup for the employees app.

# Technical: the admin site object that models are registered with.
from django.contrib import admin

from .models import Employee

# Plain English: this makes Employees show up in the built-in Django Admin site (/admin/).
# Technical: a plain register() gives stock admin pages; deliberately not customised.
admin.site.register(Employee)
