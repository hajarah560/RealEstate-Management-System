from django.db import models

# Create your models here.
class Client(models.Model):

    GENDER_OPTIONS = [
        ("M", "Male"),
        ("M", "Female")
    ]
    firstname = models.CharField(max_length= 50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, choices= GENDER_OPTIONS)
    address = models.CharField(max_length=100, null= True ,default="N/A")
    email = models.CharField()

class Employee(models.Model):
    
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("M", "Female")
    ]
    firstname = models.CharField(max_length= 50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, choices= GENDER_OPTIONS)
    address = models.CharField(max_length=100, null= True ,default="N/A")
    email = models.CharField()

class Land(models.Model):
    STATUS_OPTIONS = [
        ("T", "TAKEN"),
        ("NT","NOT TAKEN")
    ]
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length = 2, choices = STATUS_OPTIONS)
    land_size = models.CharField(max_length=40)
    land_type = models.CharField(max_length=30)
  

class Building(models.Model):
    STATUS_OPTIONS = [
        ("T", "TAKEN"),
        ("NT","NOT TAKEN")
    ]
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length = 2, choices = STATUS_OPTIONS)

class Lease(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Payment(models.Model):
    MODE_OF_PAYEMENT = [
        ("C", "Cash"),
        ("Ch", "Cheque"),
        ("Bt", "Bank Transfer")
    ]
    amount_paid = models.CharField(max_length=40)
    mode_of_payment = models.CharField(max_length=20, choices = MODE_OF_PAYEMENT)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE)
    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    


    

    