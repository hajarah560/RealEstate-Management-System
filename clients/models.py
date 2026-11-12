# Database model for a Client (a person who leases property).
# Plain English: this file describes what we store about each client.
# Technical: each class becomes a database table, each field a column.

# Plain English: the toolbox for describing database tables.
# Technical: models.Model and the field types (CharField, EmailField...) come from here.
from django.db import models


class Client(models.Model):
    # Plain English: the only allowed answers for gender, so the data stays tidy.
    # Technical: a choices list of (value stored in the database, label shown to people).
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Plain English: stores just "M" or "F", shown as a dropdown with Male/Female.
    # Technical: max_length=1 because only the short code is saved.
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    # Technical: a CharField, not a number, so leading zeros and "+" in phone numbers survive.
    contact = models.CharField(max_length=15)
    # Technical: EmailField is a text column that also checks the "name@site" format.
    email = models.EmailField()
    # Plain English: the address is optional. Technical: blank=True lets forms leave it
    # empty (stored as an empty string, which is why null=True is not needed for text).
    address = models.CharField(max_length=100, blank=True)

    # Plain English: how a client is written as text, e.g. "Jane Doe", in dropdowns,
    # messages and Django Admin. Technical: without this it would show "Client object (3)".
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
