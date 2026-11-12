# Database models for the things we lease: Land and Building (two tables in one app).

# Technical: models.Model and the field types come from here.
from django.db import models

# Plain English: both land and buildings are either Available or Taken, so the list of
# choices is written once here and shared. Technical: (stored value, label) pairs used
# by the status field of both models.
STATUS_OPTIONS = [
    ("A", "Available"),
    ("T", "Taken"),
]


class Land(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    # Technical: text, not a number, so values like "50x100 ft" or "2 acres" are allowed.
    land_size = models.CharField(max_length=40)
    land_type = models.CharField(max_length=30)
    # Plain English: money needs exact cents. Technical: DecimalField avoids float rounding errors.
    price = models.DecimalField(max_digits=14, decimal_places=2)
    # Technical: stores "A" or "T"; new records start as "A" (Available).
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="A")

    class Meta:
        # Plain English: stops Django Admin writing "Lands". Technical: sets the plural label.
        verbose_name_plural = "land"

    # Plain English: shows the land by its name in dropdowns and messages.
    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="A")

    def __str__(self):
        return self.name
