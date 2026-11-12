# Views for the Clients page. The other CRUD apps (employees, leases, payments,
# properties) follow this same pattern, so understanding this file covers them all.
#
# Pattern: the list page is a normal page. Add, edit and delete are small forms
# that open in a pop-up (modal). static/js/site.js fetches them and submits them
# in the background, which is why saves return an empty 204 instead of a redirect.

# `messages` queues the one-off "saved" / "deleted" notice shown as a toast after the reload.
from django.contrib import messages
# Every view here is for logged-in users only. Logged-out visitors go to /login/.
from django.contrib.auth.decorators import login_required
# Used to answer "saved, nothing more to show" (status 204) without rendering a page.
from django.http import HttpResponse
# get_object_or_404 gives a clean 404 page if the id in the URL does not exist.
from django.shortcuts import get_object_or_404, render
# reverse() builds URLs from route names, so no URL is hard-coded in the views.
from django.urls import reverse

from .forms import ClientForm
from .models import Client


# READ: list the clients
@login_required
def client_list(request):
    # Newest first, so a client just added appears at the top.
    clients = Client.objects.order_by("-id")

    # These keys feed templates/shared/list_base.html, the layout shared by all list pages.
    context = {
        "object_list": clients,
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
    # Reaching here means a GET, or a POST with errors. The 400 tells site.js to
    # show this form again inside the modal instead of reloading the page.
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        # instance=client makes the form update this row instead of creating a new one.
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
        # Save the name first: after delete() the object no longer prints usefully.
        name = str(client)
        client.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    # delete_note completes the warning "This also deletes ..." in the confirm modal.
    # Leases and payments go with the client because of on_delete=CASCADE in the models.
    context = {"object": client, "modal_title": "Delete client", "delete_note": "their leases and payments"}
    return render(request, "shared/modal_confirm.html", context)
