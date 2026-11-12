# Database model for a Lease (an agreement letting a client use a piece of land or a building).
# Plain English: a lease connects a client, the employee who handled it, and the property.
# Technical: it is the "middle" table; ForeignKey fields link it to the other tables.

# Technical: models.Model and the field types come from here.
from django.db import models

# These are imported so a Lease can point at them with a ForeignKey.
from clients.models import Client
from employees.models import Employee
from properties.models import Building, Land


class Lease(models.Model):
    # Plain English: if the client is deleted, their leases are deleted too (a lease
    # cannot exist without its client). Technical: on_delete=CASCADE passes the delete down.
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # Plain English: if the employee leaves and is deleted, the lease stays, it just
    # shows no employee. Technical: SET_NULL sets this column to NULL, which is why
    # null=True is required here.
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    # A lease is for land OR a building: exactly one of these is filled in
    # Plain English: so each of these two is allowed to be empty. Technical: null=True
    # allows NULL in the database, blank=True allows an empty box in forms. LeaseForm.clean()
    # enforces "exactly one". CASCADE: deleting the property deletes its leases.
    land = models.ForeignKey(Land, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    # Technical: DateField stores a date without a time.
    start_date = models.DateField()
    end_date = models.DateField()

    # Plain English: a shortcut that gives the name of whichever property this lease is for.
    # Technical: @property lets templates and __str__ use lease.property_name like a field;
    # "or" returns the land if there is one, otherwise the building.
    @property
    def property_name(self):
        return self.land or self.building

    # Plain English: how a lease is written as text, e.g. "Lease #4: Jane Doe - Plot 12".
    def __str__(self):
        return f"Lease #{self.pk}: {self.client} - {self.property_name}"
