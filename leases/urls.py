# Web addresses (routes) for the leases app.
# Plain English: each line says "when the browser asks for this address, run this view".

# Technical: path() declares one route.
from django.urls import path

# The view functions that answer the requests.
from . import views

urlpatterns = [
    # The name= values are what reverse("lease_list") and {% url %} in templates use,
    # so links are never typed by hand.
    path("leases/", views.lease_list, name="lease_list"),
    path("leases/add/", views.lease_add, name="lease_add"),
    # Plain English: <int:pk> is the id of the lease, e.g. /leases/5/edit/ is lease number 5.
    # Technical: "int" makes Django accept only whole numbers and pass them to the view as pk.
    path("leases/<int:pk>/edit/", views.lease_edit, name="lease_edit"),
    path("leases/<int:pk>/delete/", views.lease_delete, name="lease_delete"),
]
