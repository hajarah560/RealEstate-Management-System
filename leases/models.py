from django.db import models

from clients.models import Client
from employees.models import Employee
from properties.models import Building, Land


class Lease(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    # A lease is for land OR a building: exactly one of these is filled in
    land = models.ForeignKey(Land, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def property_name(self):
        return self.land or self.building

    def __str__(self):
        return f"Lease #{self.pk}: {self.client} - {self.property_name}"
