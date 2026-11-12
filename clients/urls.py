# Web addresses (routes) for the clients app.
# Plain English: each line says "when the browser asks for this address, run this view".
# Technical: these are included by the project's main urls.py.

# Technical: path() declares one route.
from django.urls import path

# The view functions that answer the requests.
from . import views

urlpatterns = [
    # The name= values are what reverse("client_list") and {% url %} in templates use,
    # so links are never typed by hand and keep working if an address changes.
    path("clients/", views.client_list, name="client_list"),
    path("clients/add/", views.client_add, name="client_add"),
    # Plain English: <int:pk> is the id of the client, e.g. /clients/5/edit/ is client number 5.
    # Technical: "int" makes Django accept only whole numbers and pass them to the view as pk.
    path("clients/<int:pk>/edit/", views.client_edit, name="client_edit"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),
]
