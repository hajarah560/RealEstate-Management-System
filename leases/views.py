from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import LeaseForm
from .models import Lease


# READ: list the leases
@login_required
def lease_list(request):
    leases = Lease.objects.select_related("client", "employee", "land", "building").order_by("-id")

    context = {
        "object_list": leases,
        "heading": "Leases",
        "add_label": "Add lease",
        "add_url": reverse("lease_add"),
    }
    return render(request, "leases/lease_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def lease_add(request):
    if request.method == "POST":
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save()
            messages.success(request, f"{lease} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = LeaseForm()

    context = {"form": form, "modal_title": "Add lease"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def lease_edit(request, pk):
    lease = get_object_or_404(Lease, pk=pk)

    if request.method == "POST":
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            lease = form.save()
            messages.success(request, f"{lease} saved")
            return HttpResponse(status=204)
    else:
        form = LeaseForm(instance=lease)

    context = {"form": form, "modal_title": f"Edit {lease}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def lease_delete(request, pk):
    lease = get_object_or_404(Lease, pk=pk)

    if request.method == "POST":
        name = str(lease)
        lease.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    context = {"object": lease, "modal_title": "Delete lease", "delete_note": "its payments"}
    return render(request, "shared/modal_confirm.html", context)
