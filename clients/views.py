# Views for the Clients page. Employees, leases, payments and properties copy this
# same pattern, so reading this file explains all of them.
#
# In plain English: the list page is a normal page. "Add", "Edit" and "Delete" open
# as small pop-up forms on top of it. Technically, static/js/site.js fetches each
# form into a <dialog> and submits it in the background, which is why a successful
# save answers with an empty 204 response instead of redirecting to another page.

# Plain English: lets us leave a one-time "saved" note for the next page to show.
# Technical: the messages framework stores it in the session; base.html renders it as a toast.
from django.contrib import messages
# Plain English: keeps strangers out. Technical: redirects anonymous users to LOGIN_URL (/login/).
from django.contrib.auth.decorators import login_required
# Plain English: lets us reply "done" without sending a page. Technical: used for the empty 204 response.
from django.http import HttpResponse
# render builds the HTML page from a template. get_object_or_404 looks up one row and
# shows a "not found" page, instead of crashing, if the id in the URL does not exist.
from django.shortcuts import get_object_or_404, render
# Plain English: turns a route's name into its web address. Technical: reverse() means
# no URL is typed by hand here, so changing urls.py cannot break these views.
from django.urls import reverse

# The form and model for this app (the dot means "from this same folder").
from .forms import ClientForm
from .models import Client


# READ: list the clients
@login_required
def client_list(request):
    # Plain English: newest clients first, so one you just added is at the top.
    # Technical: order by id descending; the query only runs when the template loops over it.
    clients = Client.objects.order_by("-id")

    # The context is the data handed to the template. These keys are what
    # templates/shared/list_base.html reads, the layout every list page shares.
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
    # Plain English: opening the form (GET) shows it empty; pressing Save (POST) sends the answers.
    if request.method == "POST":
        # Technical: bind the submitted data to the form, then validate it.
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"{client} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = ClientForm()

    context = {"form": form, "modal_title": "Add client"}
    # Plain English: we only get here when the form is being opened or had mistakes, so
    # show it again. Technical: status 400 tells site.js to redraw the form with its
    # errors inside the pop-up instead of reloading the page.
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        # Plain English: edit this existing client rather than making a new one.
        # Technical: passing instance= makes save() run an UPDATE instead of an INSERT.
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
        # Plain English: grab the name now so the message can still say who was removed.
        # Technical: after delete() the object no longer has a usable string form.
        name = str(client)
        client.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    # Plain English: the confirm pop-up warns "This also deletes their leases and
    # payments". Technical: that is true because the Lease model uses on_delete=CASCADE
    # on its client link, and Payment cascades from Lease; delete_note fills in that warning.
    context = {"object": client, "modal_title": "Delete client", "delete_note": "their leases and payments"}
    return render(request, "shared/modal_confirm.html", context)
