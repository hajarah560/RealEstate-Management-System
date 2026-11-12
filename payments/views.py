# Views for the Payments page. Plain English: this follows exactly the same pattern as
# clients/views.py (list page, plus Add / Edit / Delete pop-up forms), so read that file
# first. Technical: only the parts that differ are commented below.
# Different here: each payment is tied to a lease, and the client is reached through it.

# Imports: the same set as clients/views.py (messages, login_required, HttpResponse,
# get_object_or_404 + render, reverse). Each is explained there.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# The form and model for this app.
from .forms import PaymentForm
from .models import Payment


# READ: list the payments
@login_required
def payment_list(request):
    # Plain English: load each payment with its lease, that lease's client, and the
    # employee in one go. Technical: select_related follows the lease -> client chain with
    # the double underscore 'lease__client', because the list shows the client name
    # (Payment.__str__ also uses lease.client).
    payments = Payment.objects.select_related("lease__client", "employee").order_by("-id")

    context = {
        "object_list": payments,
        "heading": "Payments",
        "add_label": "Add payment",
        "add_url": reverse("payment_add"),
    }
    return render(request, "payments/payment_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def payment_add(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"{payment} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        # Technical: an empty PaymentForm already has today's date filled in, because the
        # model's date field has default=timezone.localdate (see payments/models.py).
        form = PaymentForm()

    context = {"form": form, "modal_title": "Add payment"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"{payment} saved")
            return HttpResponse(status=204)
    else:
        form = PaymentForm(instance=payment)

    context = {"form": form, "modal_title": f"Edit {payment}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == "POST":
        name = str(payment)
        payment.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    # Plain English: a payment is the last link in the chain, so deleting one removes
    # nothing else and no warning is needed (delete_note is empty).
    context = {"object": payment, "modal_title": "Delete payment", "delete_note": ""}
    return render(request, "shared/modal_confirm.html", context)
