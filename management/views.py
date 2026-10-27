from django.shortcuts import render

from management.forms import ClientForm

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def employee_view(request):
    return render(request, "employee.html")

def property_view(request):
    return render(request, "property.html")

def payment_view(request):
    return render(request, "payment.html")

def lease_view(request):
    return render(request, "lease.html")

def add_client_view(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)

        if client_form. is_valid():
            client_form.save()

    else:
        client_form = ClientForm()

    context = {
        'form' : client_form
    }

    return render (request, "client.html", context)
