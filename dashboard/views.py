# The Overview (home) page: a few totals plus the latest leases and payments.

# Plain English: keeps strangers out. Technical: anonymous users are sent to LOGIN_URL.
from django.contrib.auth.decorators import login_required
# Plain English: lets the database add up a column. Technical: Sum is used inside aggregate().
from django.db.models import Sum
from django.shortcuts import render
# Plain English: today's date. Technical: timezone.localdate() respects TIME_ZONE in settings.py.
from django.utils import timezone

# Every model we count or list on the Overview.
from clients.models import Client
from employees.models import Employee
from leases.models import Lease
from payments.models import Payment
from properties.models import Building, Land


# Shows the home page: totals and the latest leases and payments
@login_required
def index(request):
    # The context is the data handed to the template (keys are the names used there).
    context = {
        # Plain English: how many clients and employees we have.
        "clients": Client.objects.count(),
        "employees": Employee.objects.count(),
        # Plain English: land and buildings still available to lease. Technical: status "A"
        # means Available (the seed data uses "T" for Taken).
        "free_land": Land.objects.filter(status="A").count(),
        "free_buildings": Building.objects.filter(status="A").count(),
        # Plain English: leases that have not ended yet. Technical: end_date__gte means
        # "end date is greater than or equal to today".
        "active_leases": Lease.objects.filter(end_date__gte=timezone.localdate()).count(),
        # Plain English: total money received. Technical: with no payments, Sum returns
        # None, so "or 0" turns that into 0 and the template can still format it.
        "payments_total": Payment.objects.aggregate(total=Sum("amount"))["total"] or 0,
        # Plain English: the 5 newest payments, newest first. Technical: select_related
        # joins the lease and client in the same query, so showing each client's name does
        # not trigger one extra query per row. [:5] becomes SQL LIMIT 5.
        "recent_payments": Payment.objects.select_related("lease__client").order_by("-id")[:5],
        # Same idea for the 5 newest leases, joining the client, land and building they point to.
        "recent_leases": Lease.objects.select_related("client", "land", "building").order_by("-id")[:5],
    }
    return render(request, "dashboard/index.html", context)
