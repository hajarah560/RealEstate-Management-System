# The sign-up form for new visitors.
#
# Plain English: this decides which boxes appear on the "Create an account" page
# and checks what the visitor typed. Technical: a Django ModelForm subclass that
# builds a User row; core/views.py uses it in the sign_up view.

# Plain English: Django's toolbox for building forms. Technical: gives us CharField, EmailField, etc.
from django import forms
# Plain English: Django's ready-made sign-up form. Technical: it already handles the two
# password boxes, checks they match and runs the password-strength rules from settings.py.
from django.contrib.auth.forms import UserCreationForm
# Plain English: the table of people who can log in. Technical: the form saves into this model.
from django.contrib.auth.models import User


# Plain English: we extend (not rewrite) Django's form so we get the safe password
# handling for free and only add what we need. Technical: inheritance from UserCreationForm.
class SignUpForm(UserCreationForm):
    """Django's sign-up form plus first name, last name and email."""

    # Plain English: extra boxes the default form does not have.
    # Technical: declared here because UserCreationForm only asks for username and passwords.
    # Required by default, so the visitor cannot leave them empty.
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    # Plain English: settings about the form rather than its boxes.
    # Technical: we extend UserCreationForm.Meta so we keep its settings (for example
    # which fields use the username widget) and only override model and fields.
    class Meta(UserCreationForm.Meta):
        model = User
        # Plain English: the order here is the order the boxes appear on the page, and
        # a field must be listed here or it is not saved to the User. Technical: the
        # password boxes are added by the parent class, so they are not listed.
        fields = ("username", "first_name", "last_name", "email")
