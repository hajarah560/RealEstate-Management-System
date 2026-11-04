from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from management.forms import ClientForm, EmployeeForm, LeaseForm, LandForm, BuildingForm, PaymentForm
from management.models import Client, Employee, Lease, Land, Building, Payment


def home_view(request):
    return render(request, "home.html")


def sign_up_view(request):
    if request.method == "POST":
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            messages.success(request, "User created successfully.")
            return redirect("sign_up_page")
    else:
        sign_up_form = UserCreationForm()

    context = {'form': sign_up_form}
    return render(request, "registration/sign_up.html", context)


def add_client_view(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client_form.save()
            messages.success(request, "Client added successfully.")
            return redirect("client_page")
    else:
        client_form = ClientForm()
    context = {'form': client_form, 'clients': Client.objects.all().order_by('-id')}
    return render(request, "client.html", context)


def edit_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            messages.success(request, "Client updated successfully.")
            return redirect("client_page")
    else:
        client_form = ClientForm(instance=client)
    return render(request, "edit_record.html", {'form': client_form, 'record': client, 'record_type': 'client', 'back_url': 'client_page'})


def delete_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect("client_page")
    return render(request, "delete_record.html", {'record': client, 'record_type': 'client', 'back_url': 'client_page'})


def add_employee_view(request):
    if request.method == "POST":
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("employee_page")
    else:
        employee_form = EmployeeForm()
    context = {'form': employee_form, 'employees': Employee.objects.all().order_by('-id')}
    return render(request, "employee.html", context)


def edit_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        employee_form = EmployeeForm(request.POST, instance=employee)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employee_page")
    else:
        employee_form = EmployeeForm(instance=employee)
    return render(request, "edit_record.html", {'form': employee_form, 'record': employee, 'record_type': 'employee', 'back_url': 'employee_page'})


def delete_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect("employee_page")
    return render(request, "delete_record.html", {'record': employee, 'record_type': 'employee', 'back_url': 'employee_page'})


def add_land_view(request):
    if request.method == "POST":
        land_form = LandForm(request.POST)
        if land_form.is_valid():
            land_form.save()
            messages.success(request, "Land added successfully.")
            return redirect("land_page")
    else:
        land_form = LandForm()
    context = {'form': land_form, 'lands': Land.objects.all().order_by('-id')}
    return render(request, "land.html", context)


def edit_land_view(request, land_id):
    land = get_object_or_404(Land, id=land_id)
    if request.method == "POST":
        land_form = LandForm(request.POST, instance=land)
        if land_form.is_valid():
            land_form.save()
            messages.success(request, "Land updated successfully.")
            return redirect("land_page")
    else:
        land_form = LandForm(instance=land)
    return render(request, "edit_record.html", {'form': land_form, 'record': land, 'record_type': 'land', 'back_url': 'land_page'})


def delete_land_view(request, land_id):
    land = get_object_or_404(Land, id=land_id)
    if request.method == "POST":
        land.delete()
        messages.success(request, "Land deleted successfully.")
        return redirect("land_page")
    return render(request, "delete_record.html", {'record': land, 'record_type': 'land', 'back_url': 'land_page'})


def add_building_view(request):
    if request.method == "POST":
        building_form = BuildingForm(request.POST)
        if building_form.is_valid():
            building_form.save()
            messages.success(request, "Building added successfully.")
            return redirect("building_page")
    else:
        building_form = BuildingForm()
    context = {'form': building_form, 'buildings': Building.objects.all().order_by('-id')}
    return render(request, "building.html", context)


def edit_building_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    if request.method == "POST":
        building_form = BuildingForm(request.POST, instance=building)
        if building_form.is_valid():
            building_form.save()
            messages.success(request, "Building updated successfully.")
            return redirect("building_page")
    else:
        building_form = BuildingForm(instance=building)
    return render(request, "edit_record.html", {'form': building_form, 'record': building, 'record_type': 'building', 'back_url': 'building_page'})


def delete_building_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    if request.method == "POST":
        building.delete()
        messages.success(request, "Building deleted successfully.")
        return redirect("building_page")
    return render(request, "delete_record.html", {'record': building, 'record_type': 'building', 'back_url': 'building_page'})


def lease_view(request):
    if request.method == "POST":
        lease_form = LeaseForm(request.POST)
        if lease_form.is_valid():
            lease_form.save()
            messages.success(request, "Lease added successfully.")
            return redirect("lease_page")
    else:
        lease_form = LeaseForm()
    context = {'form': lease_form, 'leases': Lease.objects.all().order_by('-id')}
    return render(request, "lease.html", context)


def edit_lease_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == "POST":
        lease_form = LeaseForm(request.POST, instance=lease)
        if lease_form.is_valid():
            lease_form.save()
            messages.success(request, "Lease updated successfully.")
            return redirect("lease_page")
    else:
        lease_form = LeaseForm(instance=lease)
    return render(request, "edit_record.html", {'form': lease_form, 'record': lease, 'record_type': 'lease', 'back_url': 'lease_page'})


def delete_lease_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == "POST":
        lease.delete()
        messages.success(request, "Lease deleted successfully.")
        return redirect("lease_page")
    return render(request, "delete_record.html", {'record': lease, 'record_type': 'lease', 'back_url': 'lease_page'})


def payment_view(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, "Payment added successfully.")
            return redirect("payment_page")
    else:
        payment_form = PaymentForm()
    context = {'form': payment_form, 'payments': Payment.objects.all().order_by('-id')}
    return render(request, "payment.html", context)


def edit_payment_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        payment_form = PaymentForm(request.POST, instance=payment)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, "Payment updated successfully.")
            return redirect("payment_page")
    else:
        payment_form = PaymentForm(instance=payment)
    return render(request, "edit_record.html", {'form': payment_form, 'record': payment, 'record_type': 'payment', 'back_url': 'payment_page'})


def delete_payment_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        payment.delete()
        messages.success(request, "Payment deleted successfully.")
        return redirect("payment_page")
    return render(request, "delete_record.html", {'record': payment, 'record_type': 'payment', 'back_url': 'payment_page'})
