# The form used to add and edit a Client.
# Plain English: a form is the set of boxes a user fills in.
# Technical: a ModelForm builds those boxes and their validation from the model.

# Technical: provides forms.ModelForm and the widget classes.
from django import forms

# The model this form creates and edits.
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        # Plain English: only these boxes appear, in this order.
        # Technical: an explicit list is safer than "__all__", because a field added
        # to the model later will not silently show up in the form.
        fields = ["first_name", "last_name", "gender", "contact", "email", "address"]
        # Plain English: a normal one-line box for the address.
        # Technical: overrides the default widget; the address is still a one-line CharField.
        widgets = {"address": forms.TextInput()}
