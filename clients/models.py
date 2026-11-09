from django.db import models


class Client(models.Model):
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
