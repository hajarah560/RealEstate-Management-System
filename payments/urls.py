from django.urls import path

from . import views

urlpatterns = [
    path("payments/", views.payment_list, name="payment_list"),
    path("payments/add/", views.payment_add, name="payment_add"),
    path("payments/<int:pk>/edit/", views.payment_edit, name="payment_edit"),
    path("payments/<int:pk>/delete/", views.payment_delete, name="payment_delete"),
]
