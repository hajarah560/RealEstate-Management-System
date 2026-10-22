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
from django.urls import path
from management.views import index, home, client, lease, property, payment,employee

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index_page"),
    path('/home', home, name ="home_page"),
    path('/employee', employee, name="employee_page"),
    path('/client', client, name="client_page"),
    path('/property', property, name="property_page"),
    path('/payment', payment, name="payment_page"),
    path('/lease', lease, name = "lease_page")
]


