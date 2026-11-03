from django.shortcuts import render

from management.forms import ClientForm, EmployeeForm, LeaseForm, LandForm, BuildingForm, PaymentForm

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def add_land_view(request):
    return render(request, "land.html")

def add_building_view(request):
    return render(request, "building.html")

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

def add_employee_view(request):
    if request.method == "POST":
         employee_form = EmployeeForm(request.POST)
         if employee_form. is_valid():
                employee_form.save()

    else:
        employee_form = EmployeeForm()

    context = {
        'form' : employee_form
    }

    return render (request, "employee.html", context)


def add_land_view(request):
    if request.method == "POST":
         land_form = LandForm(request.POST)
         if land_form. is_valid():
                land_form.save()

    else:
        land_form = LandForm()

    context = {
        'form' : land_form
    }

    return render (request, "land.html", context)


def add_building_view(request):
    if request.method == "POST":
         building_form = BuildingForm(request.POST)
         if building_form. is_valid():
                building_form.save()

    else:
        building_form = BuildingForm()

    context = {
        'form' : building_form
    }

    return render (request, "building.html", context)


def add_lease_view(request):
    if request.method == "POST":
         lease_form = LeaseForm(request.POST)
         if lease_form. is_valid():
                lease_form.save()

    else:
        lease_form = LeaseForm()

    context = {
        'form' : lease_form
    }

    return render (request, "lease.html", context)




def add_payment_view(request):
    if request.method == "POST":
         lease_form = PaymentForm(request.POST)
         if lease_form. is_valid():
                lease_form.save()

    else:
        lease_form = PaymentForm()

    context = {
        'form' : lease_form
    }

    return render (request, "payment.html", context)



    

