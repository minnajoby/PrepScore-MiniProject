# In profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill, Education, Experience, Certification
from .forms import SkillForm, EducationForm, ExperienceForm

# --- VIEWS ---

def home_view(request):
    return render(request, 'profiles/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect('home')

def about_view(request):
    return render(request, 'profiles/about.html')

def features_view(request):
    return render(request, 'profiles/features.html')

@login_required
def dashboard_view(request):
    try:
        profile = request.user.profile
        skills = Skill.objects.filter(profile=profile)
        educations = Education.objects.filter(profile=profile)
        experiences = Experience.objects.filter(profile=profile)
        certifications = Certification.objects.filter(profile=profile)
    except Profile.DoesNotExist:
        profile = None
        skills, educations, experiences, certifications = [], [], [], []

    context = {
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'certifications': certifications,
    }
    return render(request, 'profiles/dashboard.html', context)

# --- CREATE VIEWS ---

@login_required
def add_skill_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, "Skill successfully added!")
            return redirect('dashboard')
    else:
        form = SkillForm()
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
            messages.success(request, "Education entry successfully added!")
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
            messages.success(request, "Experience entry successfully added!")
            return redirect('dashboard')
    else:
        form = ExperienceForm()
    return render(request, 'profiles/add_experience.html', {'form': form})

# --- UPDATE VIEWS ---

@login_required
def edit_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill successfully updated!")
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'profiles/edit_skill.html', {'form': form})

@login_required
def edit_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education entry successfully updated!")
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)
    return render(request, 'profiles/edit_education.html', {'form': form})

@login_required
def edit_experience_view(request, pk):
    experience = get_object_or_404(Experience, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience entry successfully updated!")
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'profiles/edit_experience.html', {'form': form})

# --- DELETE VIEWS ---

@login_required
def delete_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, "Skill has been deleted.")
        return redirect('dashboard')
    return render(request, 'profiles/confirm_delete.html', {'object': skill, 'type': 'Skill'})

@login_required
def delete_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        education.delete()
        messages.info(request, "Education entry has been deleted.")
        return redirect('dashboard')
    return render(request, 'profiles/confirm_delete.html', {'object': education, 'type': 'Education Entry'})

@login_required
def delete_experience_view(request, pk):
    experience = get_object_or_404(Experience, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        experience.delete()
        messages.info(request, "Experience entry has been deleted.")
        return redirect('dashboard')
    return render(request, 'profiles/confirm_delete.html', {'object': experience, 'type': 'Experience Entry'})
