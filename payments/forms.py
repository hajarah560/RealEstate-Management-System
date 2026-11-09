from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["lease", "employee", "amount", "mode", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
