from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "gender", "contact", "email", "address"]
        widgets = {"address": forms.TextInput()}
