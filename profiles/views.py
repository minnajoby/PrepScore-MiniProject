from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'profiles/home.html')


def register_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email already registered."
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect("login")
    return render(request, "profiles/register.html", {"error": error})

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or redirect to a dashboard page
        else:
            error = "Invalid username or password."
    return render(request, 'profiles/login.html', {'error': error})

@login_required # This is a "decorator" that protects the page
def dashboard_view(request):
    # For now, it just renders a simple template.
    # Later, we will pass data to it.
    return render(request, 'profiles/dashboard.html')
def logout_view(request):
    logout(request)
    # After logging out, redirect the user back to the homepage
    return redirect('home')