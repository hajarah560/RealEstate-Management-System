# Database model for an Employee (a staff member who handles leases and payments).
# It has the same fields as Client; see clients/models.py for the full explanation.
# Technical: each class becomes a database table, each field a column.

# Technical: models.Model and the field types come from here.
from django.db import models


class Employee(models.Model):
    # Plain English: the only allowed answers for gender.
    # Technical: choices are (value stored, label shown) pairs.
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    # blank=True: the address may be left empty in forms.
    address = models.CharField(max_length=100, blank=True)

    # Plain English: shows an employee as "First Last" instead of "Employee object (2)".
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
