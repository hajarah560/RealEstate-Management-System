from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.search import search

from .forms import ClientForm
from .models import Client


# READ: list the clients, with search
@login_required
def client_list(request):
    clients = Client.objects.order_by("-id")
    q = request.GET.get("q", "").strip()
    clients = search(clients, q, ["first_name", "last_name", "contact", "email", "address"])

    context = {
        "object_list": clients,
        "q": q,
        "heading": "Clients",
        "add_label": "Add client",
        "add_url": reverse("client_add"),
    }
    return render(request, "clients/client_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def client_add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"{client} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = ClientForm()

    context = {"form": form, "modal_title": "Add client"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"{client} saved")
            return HttpResponse(status=204)
    else:
        form = ClientForm(instance=client)

    context = {"form": form, "modal_title": f"Edit {client}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        name = str(client)
        client.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    context = {"object": client, "modal_title": "Delete client", "delete_note": "their leases and payments"}
    return render(request, "shared/modal_confirm.html", context)
