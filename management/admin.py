from django.contrib import admin

from .models import Client, Employee, Building, Land, Lease, Payment

# Register your models here.
class Clients(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "contact", "gender", "address", "email")

class Employees(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "contact", "gender", "address", "email")

class Buildings(admin.ModelAdmin):
    list_display = ("name", )

class admin_Land(admin.ModelAdmin):
    list_display = ("land_size", "land_type", )

class admin_Lease(admin.ModelAdmin):
    list_display = ("client", "employee", )

class admin_Payment(admin.ModelAdmin):
    list_display = ("amount_paid", "mode_of_payment", "employee", "client")

admin.site.register(Client, Clients)
admin.site.register(Employee, Employees)
admin.site.register(Building, Buildings)
admin.site.register(Land, admin_Land)
admin.site.register(Lease, admin_Lease)
admin.site.register(Payment, admin_Payment)





