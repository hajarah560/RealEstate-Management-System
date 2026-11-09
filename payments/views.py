from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import PaymentForm
from .models import Payment


# READ: list the payments
@login_required
def payment_list(request):
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

    context = {"object": payment, "modal_title": "Delete payment", "delete_note": ""}
    return render(request, "shared/modal_confirm.html", context)
