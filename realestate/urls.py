# The project's address book: which web address runs which view.
#
# Plain English: when someone visits /login/, Django reads this list from top to
# bottom and runs the first entry that matches. Technical: ROOT_URLCONF in
# settings.py points here.

# Plain English: Django's built-in admin site. Technical: admin.site.urls provides all /admin/ routes.
from django.contrib import admin
# Plain English: Django's ready-made login and logout pages. Technical: class-based views.
from django.contrib.auth import views as auth_views
# path() defines one route; include() pulls in another file's list of routes.
from django.urls import include, path

# Our own views, imported under short names so the two "views" modules do not clash.
from core import views as core_views
from dashboard import views as dashboard_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Plain English: a logged-in person who opens /login/ is sent on to the Overview
    # instead of seeing the form again. Technical: redirect_authenticated_user=True
    # redirects to LOGIN_REDIRECT_URL (see settings.py).
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    # Plain English: login and logout are the same in every Django site, so we reuse
    # Django's tested views. Technical: sign_up is our own view because Django has no
    # built-in sign-up page (and ours must also log the user in and ask for name/email).
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("sign_up/", core_views.sign_up, name="sign_up"),
    path("", dashboard_views.index, name="dashboard"),

    # Each app's urls.py lists its own list/add/edit/delete routes.
    # Plain English: the "" prefix means these pages sit at the top level (/clients/, not
    # /something/clients/). Technical: include() adds each app's routes after an empty
    # prefix; the apps' own paths already start with their name, so they do not collide.
    path("", include("clients.urls")),
    path("", include("employees.urls")),
    path("", include("properties.urls")),
    path("", include("leases.urls")),
    path("", include("payments.urls")),
]
