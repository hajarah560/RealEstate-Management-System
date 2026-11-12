# The sign-up page. (Log in and log out use Django's built-in views, see realestate/urls.py.)

# Plain English: lets us leave a one-time note for the next page. Technical: the messages
# framework; base.html shows it as a toast.
from django.contrib import messages
# Plain English: marks the new user as logged in. Technical: login() stores the user's id in the session.
from django.contrib.auth import login
# redirect sends the browser to another page by route name; render builds a page from a template.
from django.shortcuts import redirect, render

# The sign-up form from this same folder.
from .forms import SignUpForm


def sign_up(request):
    # Sign-up is for visitors only. Anyone already logged in goes to the Overview.
    # Plain English: someone who is already in has no reason to make a second account.
    # Technical: request.user.is_authenticated is True once a session login exists.
    if request.user.is_authenticated:
        return redirect("dashboard")

    # Plain English: GET shows the empty form, POST means the visitor pressed the button.
    if request.method == "POST":
        # Technical: bind the submitted data to the form, then validate it.
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Plain English: log them in straight away so they do not have to type the
            # same details again on the login page. Technical: save() only creates the
            # row; login() is what attaches it to this browser's session.
            login(request, user)
            # Plain English: a friendly greeting shown once on the next page.
            messages.success(request, f"Welcome, {user.first_name}. Your account is ready.")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    # If the form was invalid we fall through to here and redraw it with the error messages.
    return render(request, "registration/sign_up.html", {"form": form})
