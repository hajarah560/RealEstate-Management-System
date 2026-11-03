from django.forms import ModelForm

from management.models import Client, Employee ,Payment, Lease, Building, Land

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = "__all__"

class LandForm(ModelForm):
    class Meta:
        model = Land
        fields ="__all__"

class LeaseForm(ModelForm):
    class Meta:
        model = Lease
        fields = "__all__"