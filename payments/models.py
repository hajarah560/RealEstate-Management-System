from django.db import models
from django.utils import timezone

from employees.models import Employee
from leases.models import Lease


class Payment(models.Model):
    MODE_OPTIONS = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    mode = models.CharField(max_length=20, choices=MODE_OPTIONS)
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"Payment #{self.pk}: {self.lease.client}"
