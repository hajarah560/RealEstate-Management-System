# Web addresses (routes) for the payments app.
# Plain English: each line says "when the browser asks for this address, run this view".

# Technical: path() declares one route.
from django.urls import path

# The view functions that answer the requests.
from . import views

urlpatterns = [
    # The name= values are what reverse("payment_list") and {% url %} in templates use,
    # so links are never typed by hand.
    path("payments/", views.payment_list, name="payment_list"),
    path("payments/add/", views.payment_add, name="payment_add"),
    # Plain English: <int:pk> is the id of the payment, e.g. /payments/5/edit/ is payment number 5.
    # Technical: "int" makes Django accept only whole numbers and pass them to the view as pk.
    path("payments/<int:pk>/edit/", views.payment_edit, name="payment_edit"),
    path("payments/<int:pk>/delete/", views.payment_delete, name="payment_delete"),
]
