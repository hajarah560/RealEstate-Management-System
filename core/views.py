from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


def sign_up(request):
    # Sign-up is for visitors only. Anyone already logged in goes to the Overview.
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}. Your account is ready.")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})
