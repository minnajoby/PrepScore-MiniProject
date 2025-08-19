# In profiles/views.py

from django.shortcuts import render, redirect,get_object_or_404
# Import everything needed in one place
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Import the form that was missing
from django.contrib.auth.forms import AuthenticationForm 
from .models import Profile, Skill, Education, Experience, Certification
from .forms import SkillForm,EducationForm,ExperienceForm



# --- VIEWS ---

def home_view(request):
    return render(request, 'profiles/home.html')


# --- CORRECTED register_view ---
def register_view(request):
    error = None
    if request.method == "POST":
        # Get the data from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password") # Assuming the password field is named 'password'
        
        # --- Start of validation ---
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        # You could add password length validation here if you wanted
        # elif len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        else:
            # --- If all validation passes, create the user ---
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # --- FIX 1: Log the user in immediately after creation ---
            login(request, user)
            
            messages.success(request, f"Account created successfully! Welcome, {username}.")
            # Redirect to the dashboard, not the login page
            return redirect("dashboard")
            
    # If there was an error, the function will continue and render the page again
    return render(request, "profiles/register.html")


# --- Your login_view is already good ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})


# --- FIX 2: A secure logout_view that requires a POST request ---
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    # If it's a GET request, it will do nothing and just redirect to home
    return redirect('home')
@login_required
def dashboard_view(request):
    # --- ALL OF THIS LOGIC IS NOW CORRECTLY INDENTED ---
    try:
        # Get the Profile linked to the currently logged-in user
        profile = request.user.profile
        
        # Fetch related data sets
        skills = Skill.objects.filter(profile=profile)
        educations = Education.objects.filter(profile=profile)
        experiences = Experience.objects.filter(profile=profile)
        certifications = Certification.objects.filter(profile=profile)

    except Profile.DoesNotExist:
        # Handle case where user exists but a profile is not yet created
        profile = None
        skills = []
        educations = []
        experiences = []
        certifications = []

    # Bundle data to send to the template
    context = {
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'certifications': certifications,
    }

    # Pass the context to the template
    return render(request, 'profiles/dashboard.html', context)
@login_required
def add_skill_view(request):
    # A user might not have a profile yet, so we need to handle that.
    # This will create a Profile object for the user if one doesn't exist.
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False) # Don't save to the DB just yet
            skill.profile = profile         # Set the profile to the logged-in user's profile
            skill.save()                    # Now, save it to the database
            return redirect('dashboard')    # Redirect back to the dashboard after success
    else:
        form = SkillForm() # If it's a GET request, create a blank form

    return render(request, 'profiles/add_skill.html', {'form': form})
@login_required
def add_education_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            return redirect('dashboard')
    else:
        form = EducationForm()

    return render(request, 'profiles/add_education.html', {'form': form})
@login_required
def add_experience_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            return redirect('dashboard')
    else:
        form = ExperienceForm()
@login_required
def edit_skill_view(request, pk):
    # Get the specific skill we want to edit, ensuring it belongs to the logged-in user
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)

    if request.method == 'POST':
        # Pass 'instance=skill' to pre-populate the form with the skill's current data
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save() # Save the changes to the existing skill object
            return redirect('dashboard')
    else:
        # If it's a GET request, create the form pre-populated with the skill's data
        form = SkillForm(instance=skill)

    return render(request, 'profiles/edit_skill.html', {'form': form})

    return render(request, 'profiles/add_experience.html', {'form': form})
