from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core import views as core_views
from dashboard import views as dashboard_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("sign_up/", core_views.sign_up, name="sign_up"),
    path("", dashboard_views.index, name="dashboard"),

    # Each app's urls.py lists its own list/add/edit/delete routes.
    path("", include("clients.urls")),
    path("", include("employees.urls")),
    path("", include("properties.urls")),
    path("", include("leases.urls")),
    path("", include("payments.urls")),
]
