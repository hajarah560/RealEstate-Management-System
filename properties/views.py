from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.search import search

from .forms import LandForm, BuildingForm
from .models import Land, Building


# READ: list the lands, with search
@login_required
def land_list(request):
    lands = Land.objects.order_by("-id")
    q = request.GET.get("q", "").strip()
    lands = search(lands, q, ["name", "location", "land_type", "land_size"])

    context = {
        "object_list": lands,
        "q": q,
        "heading": "Land",
        "add_label": "Add land",
        "add_url": reverse("land_add"),
    }
    return render(request, "properties/land_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def land_add(request):
    if request.method == "POST":
        form = LandForm(request.POST)
        if form.is_valid():
            land = form.save()
            messages.success(request, f"{land} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = LandForm()

    context = {"form": form, "modal_title": "Add land"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def land_edit(request, pk):
    land = get_object_or_404(Land, pk=pk)

    if request.method == "POST":
        form = LandForm(request.POST, instance=land)
        if form.is_valid():
            land = form.save()
            messages.success(request, f"{land} saved")
            return HttpResponse(status=204)
    else:
        form = LandForm(instance=land)

    context = {"form": form, "modal_title": f"Edit {land}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def land_delete(request, pk):
    land = get_object_or_404(Land, pk=pk)

    if request.method == "POST":
        name = str(land)
        land.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    context = {"object": land, "modal_title": "Delete land", "delete_note": "its leases and their payments"}
    return render(request, "shared/modal_confirm.html", context)


# READ: list the buildings, with search
@login_required
def building_list(request):
    buildings = Building.objects.order_by("-id")
    q = request.GET.get("q", "").strip()
    buildings = search(buildings, q, ["name", "location"])

    context = {
        "object_list": buildings,
        "q": q,
        "heading": "Buildings",
        "add_label": "Add building",
        "add_url": reverse("building_add"),
    }
    return render(request, "properties/building_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def building_add(request):
    if request.method == "POST":
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save()
            messages.success(request, f"{building} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = BuildingForm()

    context = {"form": form, "modal_title": "Add building"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk)

    if request.method == "POST":
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            building = form.save()
            messages.success(request, f"{building} saved")
            return HttpResponse(status=204)
    else:
        form = BuildingForm(instance=building)

    context = {"form": form, "modal_title": f"Edit {building}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk)

    if request.method == "POST":
        name = str(building)
        building.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    context = {"object": building, "modal_title": "Delete building", "delete_note": "its leases and their payments"}
    return render(request, "shared/modal_confirm.html", context)
