from django.contrib import admin

from .models import Client, Employee, Property, Building, Land, Lease, Payment

# Register your models here.
class Clients(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "contact", "gender", "address", "email")

class Employees(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "contact", "gender", "address", "email")

class Properties(admin.ModelAdmin):
    list_display = ("name", "location", "status")

class Buildings(admin.ModelAdmin):
    list_display = ("name", "property")

class admin_Land(admin.ModelAdmin):
    list_display = ("land_size", "land_type", "property")

class admin_Lease(admin.ModelAdmin):
    list_display = ("client", "employee", "property")

class admin_Payment(admin.ModelAdmin):
    list_display = ("amount_paid", "mode_of_payment", "property", "employee", "client")

admin.site.register(Client, Clients)
admin.site.register(Employee, Employees)
admin.site.register(Property, Properties)
admin.site.register(Building, Buildings)
admin.site.register(Land, admin_Land)
admin.site.register(Lease, admin_Lease)
admin.site.register(Payment, admin_Payment)





