from django.forms import ModelForm

from management.models import Client  #, Building, Property, Lease, Payment, Land

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"