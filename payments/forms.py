# The form used to add and edit a Payment.

# Technical: provides forms.ModelForm and the widget classes.
from django import forms

# The model this form creates and edits.
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        # Technical: explicit list of the boxes shown, in order.
        fields = ["lease", "employee", "amount", "mode", "date"]
        # Plain English: a calendar picker for the date. Technical: type="date" renders
        # <input type="date">, which only accepts the value in YYYY-MM-DD form, so
        # format="%Y-%m-%d" is needed or the default/existing date would show up blank.
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
