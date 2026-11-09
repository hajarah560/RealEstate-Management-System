from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import EmployeeForm
from .models import Employee


# READ: list the employees
@login_required
def employee_list(request):
    employees = Employee.objects.order_by("-id")

    context = {
        "object_list": employees,
        "heading": "Employees",
        "add_label": "Add employee",
        "add_url": reverse("employee_add"),
    }
    return render(request, "employees/employee_list.html", context)


# CREATE: show the empty form (GET) or save it (POST)
@login_required
def employee_add(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"{employee} saved")
            return HttpResponse(status=204)  # site.js reloads the page on 204
    else:
        form = EmployeeForm()

    context = {"form": form, "modal_title": "Add employee"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# UPDATE: show the form filled in (GET) or save the changes (POST)
@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"{employee} saved")
            return HttpResponse(status=204)
    else:
        form = EmployeeForm(instance=employee)

    context = {"form": form, "modal_title": f"Edit {employee}"}
    return render(request, "shared/modal_form.html", context, status=400 if form.errors else 200)


# DELETE: ask for confirmation (GET) or delete (POST)
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        name = str(employee)
        employee.delete()
        messages.success(request, f"{name} deleted")
        return HttpResponse(status=204)

    context = {"object": employee, "modal_title": "Delete employee", "delete_note": ""}
    return render(request, "shared/modal_confirm.html", context)
