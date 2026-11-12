# The forms used to add and edit Land and Buildings (one form per model).

# Technical: provides forms.ModelForm.
from django import forms

# The two models these forms create and edit.
from .models import Building, Land


class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        # Technical: explicit list of the boxes shown, in order.
        fields = ["name", "location", "land_size", "land_type", "price", "status"]


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        # A building has no size/type boxes, so its list is shorter.
        fields = ["name", "location", "price", "status"]
