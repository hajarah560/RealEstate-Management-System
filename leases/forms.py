from django import forms

from .models import Lease


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ["client", "employee", "land", "building", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    # A lease needs exactly one of land or building, and the dates must be in order
    def clean(self):
        data = super().clean()
        if bool(data.get("land")) == bool(data.get("building")):
            raise forms.ValidationError("Choose either a land or a building (not both, not neither).")
        if data.get("start_date") and data.get("end_date") and data["end_date"] < data["start_date"]:
            raise forms.ValidationError("The end date cannot be before the start date.")
        return data
