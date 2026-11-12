# Database model for a Payment (money a client paid towards a lease).

# Technical: models.Model and the field types come from here.
from django.db import models
# Plain English: gives us today's date. Technical: timezone-aware, so "today" follows
# the project TIME_ZONE setting instead of the server clock.
from django.utils import timezone

# Imported so a Payment can point at them with a ForeignKey.
from employees.models import Employee
from leases.models import Lease


class Payment(models.Model):
    # Plain English: the only allowed ways of paying. Technical: (stored value, label) pairs,
    # shown as a dropdown; here both halves are the same text.
    MODE_OPTIONS = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    # Plain English: a payment belongs to a lease; delete the lease and its payments go too.
    # Technical: CASCADE. (Deleting a client cascades to leases, then to payments.)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    # Plain English: if the employee is deleted, the payment record stays with no employee.
    # Technical: SET_NULL needs null=True.
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    # Plain English: money needs exact cents. Technical: DecimalField stores exact decimals;
    # a float can give 0.1 + 0.2 = 0.30000000000000004. Up to 14 digits, 2 after the point.
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    mode = models.CharField(max_length=20, choices=MODE_OPTIONS)
    # Plain English: the date box starts as today. Technical: default is the function
    # itself (no brackets), so it is called each time a payment is made, not once at startup.
    date = models.DateField(default=timezone.localdate)

    # Plain English: shows a payment as "Payment #3: Jane Doe". The client is reached
    # through the lease (payment -> lease -> client).
    def __str__(self):
        return f"Payment #{self.pk}: {self.lease.client}"
