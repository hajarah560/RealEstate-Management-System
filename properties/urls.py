from django.urls import path

from . import views

urlpatterns = [
    path("land/", views.land_list, name="land_list"),
    path("land/add/", views.land_add, name="land_add"),
    path("land/<int:pk>/edit/", views.land_edit, name="land_edit"),
    path("land/<int:pk>/delete/", views.land_delete, name="land_delete"),
    path("buildings/", views.building_list, name="building_list"),
    path("buildings/add/", views.building_add, name="building_add"),
    path("buildings/<int:pk>/edit/", views.building_edit, name="building_edit"),
    path("buildings/<int:pk>/delete/", views.building_delete, name="building_delete"),
]
