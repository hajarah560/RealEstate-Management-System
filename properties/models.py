from django.db import models

STATUS_OPTIONS = [
    ("A", "Available"),
    ("T", "Taken"),
]


class Land(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    land_size = models.CharField(max_length=40)
    land_type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="A")

    class Meta:
        verbose_name_plural = "land"

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="A")

    def __str__(self):
        return self.name
