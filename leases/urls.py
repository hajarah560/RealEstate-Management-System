from django.urls import path

from . import views

urlpatterns = [
    path("leases/", views.lease_list, name="lease_list"),
    path("leases/add/", views.lease_add, name="lease_add"),
    path("leases/<int:pk>/edit/", views.lease_edit, name="lease_edit"),
    path("leases/<int:pk>/delete/", views.lease_delete, name="lease_delete"),
]
