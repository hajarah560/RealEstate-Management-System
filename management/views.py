from django.shortcuts import render

# Create your views here.

def index (request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def employee(request):
    return render(request, "employee.html")

def client(request):
    return render(request, "client.html")

def property(request):
    return render(request, "property.html")

def payment(request):
    return render(request, "payment.html")

def lease(request):
    return render(request, "lease.html")
