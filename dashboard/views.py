from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from clients.models import Client
from employees.models import Employee
from leases.models import Lease
from payments.models import Payment
from properties.models import Building, Land


# Shows the home page: totals and the latest leases and payments
@login_required
def index(request):
    context = {
        "clients": Client.objects.count(),
        "employees": Employee.objects.count(),
        "free_land": Land.objects.filter(status="A").count(),
        "free_buildings": Building.objects.filter(status="A").count(),
        "active_leases": Lease.objects.filter(end_date__gte=timezone.localdate()).count(),
        "payments_total": Payment.objects.aggregate(total=Sum("amount"))["total"] or 0,
        "recent_payments": Payment.objects.select_related("lease__client").order_by("-id")[:5],
        "recent_leases": Lease.objects.select_related("client", "land", "building").order_by("-id")[:5],
    }
    return render(request, "dashboard/index.html", context)
