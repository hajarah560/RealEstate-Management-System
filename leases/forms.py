# The form used to add and edit a Lease, including the rules a lease must follow.

# Technical: provides forms.ModelForm, widgets and ValidationError.
from django import forms

# The model this form creates and edits.
from .models import Lease


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        # Technical: explicit list; both land and building are included, the user picks one.
        fields = ["client", "employee", "land", "building", "start_date", "end_date"]
        # Plain English: shows a calendar date picker instead of a plain text box.
        # Technical: type="date" makes the browser render <input type="date">.
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    # A lease needs exactly one of land or building, and the dates must be in order
    # Plain English: rules that involve more than one box cannot be checked box by box,
    # so they are checked here after each box passes its own checks.
    # Technical: clean() runs during is_valid(); raising ValidationError blocks the save
    # and shows the message in the form.
    def clean(self):
        data = super().clean()
        # Plain English: land and building must not both be filled, or both be empty.
        # Technical: bool(...) turns each choice into True/False; equal values mean invalid (XOR).
        if bool(data.get("land")) == bool(data.get("building")):
            raise forms.ValidationError("Choose either a land or a building (not both, not neither).")
        # Technical: .get() and the "and" checks skip this rule if a date was already invalid.
        if data.get("start_date") and data.get("end_date") and data["end_date"] < data["start_date"]:
            raise forms.ValidationError("The end date cannot be before the start date.")
        return data
