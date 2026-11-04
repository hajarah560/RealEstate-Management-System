"""
URL configuration for realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_view, name='home_page'),
    path('sign_up/', views.sign_up_view, name='sign_up_page'),
    path('client/', views.add_client_view, name='client_page'),
    path('client/<int:client_id>/edit/', views.edit_client_view, name='edit_client_page'),
    path('client/<int:client_id>/delete/', views.delete_client_view, name='delete_client_page'),
    path('employee/', views.add_employee_view, name='employee_page'),
    path('employee/<int:employee_id>/edit/', views.edit_employee_view, name='edit_employee_page'),
    path('employee/<int:employee_id>/delete/', views.delete_employee_view, name='delete_employee_page'),
    path('land/', views.add_land_view, name='land_page'),
    path('land/<int:land_id>/edit/', views.edit_land_view, name='edit_land_page'),
    path('land/<int:land_id>/delete/', views.delete_land_view, name='delete_land_page'),
    path('building/', views.add_building_view, name='building_page'),
    path('building/<int:building_id>/edit/', views.edit_building_view, name='edit_building_page'),
    path('building/<int:building_id>/delete/', views.delete_building_view, name='delete_building_page'),
    path('lease/', views.lease_view, name='lease_page'),
    path('lease/<int:lease_id>/edit/', views.edit_lease_view, name='edit_lease_page'),
    path('lease/<int:lease_id>/delete/', views.delete_lease_view, name='delete_lease_page'),
    path('payment/', views.payment_view, name='payment_page'),
    path('payment/<int:payment_id>/edit/', views.edit_payment_view, name='edit_payment_page'),
    path('payment/<int:payment_id>/delete/', views.delete_payment_view, name='delete_payment_page'),
]
