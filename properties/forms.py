from django import forms

from .models import Building, Land


class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ["name", "location", "land_size", "land_type", "price", "status"]


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ["name", "location", "price", "status"]
