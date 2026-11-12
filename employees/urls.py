# Web addresses (routes) for the employees app.
# Plain English: each line says "when the browser asks for this address, run this view".
# Technical: these are included by the project's main urls.py.

# Technical: path() declares one route.
from django.urls import path

# The view functions that answer the requests.
from . import views

urlpatterns = [
    # The name= values are what reverse("employee_list") and {% url %} in templates use,
    # so links are never typed by hand and keep working if an address changes.
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.employee_add, name="employee_add"),
    # Plain English: <int:pk> is the id of the employee, e.g. /employees/5/edit/ is employee number 5.
    # Technical: "int" makes Django accept only whole numbers and pass them to the view as pk.
    path("employees/<int:pk>/edit/", views.employee_edit, name="employee_edit"),
    path("employees/<int:pk>/delete/", views.employee_delete, name="employee_delete"),
]
