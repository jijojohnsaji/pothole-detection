from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterForm, LoginForm


def register_view(request):
    """
    Register a new user and redirect to login page.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Extra safety checks
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "users/register.html", {"form": form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "users/register.html", {"form": form})

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Registration successful. Please login.")
            return redirect("login")

        # If form invalid
        messages.error(request, "Please correct the errors below.")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """
    Log user in and redirect to route map journey page.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, f"Welcome {user.username}!")
            return redirect("/detection/route-map/")

        # If login failed
        messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """
    Logout and redirect to login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")