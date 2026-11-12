# The form used to add and edit an Employee (same shape as clients/forms.py).

# Technical: provides forms.ModelForm and the widget classes.
from django import forms

# The model this form creates and edits.
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # Technical: an explicit fields list, so new model fields never appear by accident.
        fields = ["first_name", "last_name", "gender", "contact", "email", "address"]
        # A normal one-line box for the address.
        widgets = {"address": forms.TextInput()}
