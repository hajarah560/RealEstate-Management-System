from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})
