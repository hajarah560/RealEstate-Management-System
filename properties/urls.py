# Web addresses (routes) for the properties app: one set for land, one for buildings.
# Plain English: each line says "when the browser asks for this address, run this view".

# Technical: path() declares one route.
from django.urls import path

# The view functions that answer the requests.
from . import views

urlpatterns = [
    # The name= values are what reverse() and {% url %} in templates use, so links are
    # never typed by hand and keep working if an address changes.
    path("land/", views.land_list, name="land_list"),
    path("land/add/", views.land_add, name="land_add"),
    # Plain English: <int:pk> is the id of the land, e.g. /land/5/edit/ is land number 5.
    # Technical: "int" makes Django accept only whole numbers and pass them to the view as pk.
    path("land/<int:pk>/edit/", views.land_edit, name="land_edit"),
    path("land/<int:pk>/delete/", views.land_delete, name="land_delete"),
    # The same four routes again for buildings.
    path("buildings/", views.building_list, name="building_list"),
    path("buildings/add/", views.building_add, name="building_add"),
    path("buildings/<int:pk>/edit/", views.building_edit, name="building_edit"),
    path("buildings/<int:pk>/delete/", views.building_delete, name="building_delete"),
]
