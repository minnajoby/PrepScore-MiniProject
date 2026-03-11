# In profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill, Experience, Certification, Education, Project
from .forms import (
    LoginForm, ProfileForm, SkillForm, ExperienceForm,
    CertificationForm, CustomUserCreationForm, EducationForm, ProjectForm
)
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .scorer import calculate_ml_score, get_suggestions,get_score_contributions

# --- VIEWS ---

def home_view(request):
    return render(request, 'profiles/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # --- THIS IS THE FIX ---
            # Manually set the backend that this user should be associated with.
            # We use the path to your custom backend from settings.py.
            user.backend = 'profiles.backends.EmailOrUsernameBackend'
            # --- END OF FIX ---

            login(request, user) # Now the login function knows which backend to use
            
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('dashboard')
        else:
            # Instead of looping messages, just let the template render the form errors directly
            messages.error(request, "Please correct the errors below.")
            
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'profiles/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # Use your custom LoginForm
        if form.is_valid():
            login_credential = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            
            # 'authenticate' will now correctly use your custom backend
            user = authenticate(request, username=login_credential, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard') # Redirect on success
            else:
                messages.error(request, "Invalid username/email or password.")
                # Re-render the page with the error
                return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()
        
    return render(request, 'registration/login.html', {'form': form})

def about_view(request):
    return render(request, 'profiles/about.html')

def features_view(request):
    return render(request, 'profiles/features.html')

@login_required
def dashboard_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    skills = Skill.objects.filter(profile=profile)
    experiences = Experience.objects.filter(profile=profile)
    certifications = Certification.objects.filter(profile=profile)
    
    score = calculate_ml_score(profile)
    suggestions = get_suggestions(profile, score)
    score_contributions = get_score_contributions(profile)

    context = {
        'profile': profile, 'skills': skills,
        'experiences': experiences, 'certifications': certifications,
        'educations': Education.objects.filter(profile=profile),
        'projects': Project.objects.filter(profile=profile),
        'score': score, 'suggestions': suggestions,
        'score_contributions': score_contributions,
    }
    return render(request, 'profiles/dashboard.html', context)

# --- UPDATE VIEWS ---

@login_required
def edit_skill_view(request, pk):
    # Get the object we are editing
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)

    # Handle the POST request first
    if request.method == 'POST':
        # Create a form instance with the submitted data and the existing object
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f"Skill '{skill.name}' was updated successfully!")
            return redirect('manage_skills') # Redirect to the management page
        # If the form is NOT valid, the code will continue to the bottom
    
    # For a GET request OR a failed POST request:
    else:
        # For a GET, create a blank form pre-filled with the object's data
        form = SkillForm(instance=skill)
    
    # Always define the context before rendering
    context = {
        'form': form,
        'form_title': f'Edit Skill: {skill.name}',
        'form_subtitle': 'Update the name of your skill.',
        'submit_button_text': 'Update Skill'
    }
    
    # Render the template with the context
    return render(request, 'profiles/light_form_template.html', context)

@login_required
def edit_experience_view(request, pk):
    # Get the object we are editing
    experience = get_object_or_404(Experience, pk=pk, profile__user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, f"Experience entry for '{experience.title}' was updated successfully!")
            return redirect('manage_experience')
    else:
        form = ExperienceForm(instance=experience)
    
    context = {
        'form': form,
        'form_title': f'Edit Experience: {experience.title}',
        'form_subtitle': 'Update the details of your work experience.',
        'submit_button_text': 'Update Experience'
    }
    
    return render(request, 'profiles/light_form_template.html', context)
# --- DELETE VIEWS ---

@login_required
def delete_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, "Skill has been deleted.")
        return redirect('manage_skills')
    return render(request, 'profiles/confirm_delete.html', {'object': skill, 'type': 'Skill'})

@login_required
def delete_experience_view(request, pk):
    experience = get_object_or_404(Experience, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        experience.delete()
        messages.info(request, "Experience entry has been deleted.")
        return redirect('manage_experience')
    return render(request, 'profiles/confirm_delete.html', {'object': experience, 'type': 'Experience Entry'})

@login_required
def manage_profile_view(request):
    # Get or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Check if a new file is actually being uploaded
        new_resume_uploaded = 'resume_pdf' in request.FILES

        # Populate the form with submitted data AND the existing profile instance
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            # If a new PDF was uploaded, process it for AI Gap Analysis right now
            if new_resume_uploaded and profile.resume_pdf:
                try:
                    from ai_engine.utils import extract_text_from_pdf, generate_embedding
                    
                    extracted_text = extract_text_from_pdf(profile.resume_pdf.path)
                    if extracted_text:
                        embedding = generate_embedding(extracted_text[:8000])
                        if embedding:
                            # Save directly to Profile model!
                            profile.resume_text = extracted_text
                            profile.resume_embedding = embedding
                            profile.save()
                            messages.success(request, "Profile updated and Resume processed for AI successfully!")
                        else:
                            messages.warning(request, "Profile updated, but we couldn't generate an AI embedding for your resume.")
                    else:
                        messages.warning(request, "Profile updated, but we couldn't read the text in your PDF.")
                except Exception as e:
                    messages.warning(request, f"Profile updated, but resume processing failed: {str(e)}")
            else:
                messages.success(request, "Your profile has been updated successfully!")

            # Stay on the edit profile page
            return redirect('manage_profile')
    else:
        # For a GET request, populate the form with the profile's current data
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/manage_profile.html', {'form': form})

@login_required
def manage_skills_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, "New skill successfully added!")
            return redirect('manage_skills') # Redirect back to the same page
    else:
        form = SkillForm() # A blank form for GET requests

    # Get the list of all existing skills for this user
    skills = Skill.objects.filter(profile=profile)
    
    context = {
        'form': form,
        'skills': skills
    }
    return render(request, 'profiles/manage_skills.html', context)

@login_required
def manage_experience_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            messages.success(request, "New experience entry successfully added!")
            return redirect('manage_experience')
    else:
        form = ExperienceForm()
    experiences = Experience.objects.filter(profile=profile)
    context = {'form': form, 'experiences': experiences}
    return render(request, 'profiles/manage_experience.html', context)

@login_required
def manage_certifications_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.profile = profile
            certification.save()
            messages.success(request, "New certification successfully added!")
            return redirect('manage_certifications')
    else:
        form = CertificationForm()
    certifications = Certification.objects.filter(profile=profile)
    context = {'form': form, 'certifications': certifications}
    return render(request, 'profiles/manage_certifications.html', context)

@login_required
def edit_certification_view(request, pk):
    # Get the specific certification, ensuring it belongs to the logged-in user for security
    certification = get_object_or_404(Certification, pk=pk, profile__user=request.user)

    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification successfully updated!")
            return redirect('manage_certifications') # Redirect back to the main management page
    else:
        # For a GET request, create the form pre-populated with the certification's data
        form = CertificationForm(instance=certification)

    context = {
        'form': form,
        'form_title': 'Edit Certification',
        'submit_button_text': 'Update Certification'
    }
    # We can reuse our generic form template!
    return render(request, 'profiles/light_form_template.html', context)

@login_required
def delete_certification_view(request, pk):
    certification = get_object_or_404(Certification, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        certification.delete()
        messages.info(request, "Certification has been deleted.")
        return redirect('manage_certifications')
    
    # We can reuse the generic delete confirmation template
    return render(request, 'profiles/confirm_delete.html', {'object': certification, 'type': 'Certification'})

@login_required
def manage_education_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    educations = Education.objects.filter(profile=profile)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            messages.success(request, f"Education at '{education.school}' added!")
            return redirect('manage_education')
    else:
        form = EducationForm()
    
    return render(request, 'profiles/manage_education.html', {
        'educations': educations,
        'form': form,
        'profile': profile,
    })

@login_required
def edit_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education entry updated!")
            return redirect('manage_education')
    else:
        form = EducationForm(instance=education)
    
    context = {
        'form': form,
        'form_title': 'Edit Education',
        'submit_button_text': 'Update'
    }
    return render(request, 'profiles/light_form_template.html', context)

@login_required
def delete_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        education.delete()
        messages.info(request, "Education entry deleted.")
        return redirect('manage_education')
    return render(request, 'profiles/confirm_delete.html', {'object': education, 'type': 'Education Entry'})

@login_required
def manage_projects_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            messages.success(request, "New project successfully added!")
            return redirect('manage_projects')
    else:
        form = ProjectForm()
    projects = Project.objects.filter(profile=profile)
    context = {'form': form, 'projects': projects}
    return render(request, 'profiles/manage_projects.html', context)

@login_required
def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project successfully updated!")
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'form_title': 'Edit Project',
        'submit_button_text': 'Update'
    }
    return render(request, 'profiles/light_form_template.html', context)

@login_required
def delete_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        project.delete()
        messages.info(request, "Project deleted.")
        return redirect('manage_projects')
    return render(request, 'profiles/confirm_delete.html', {'object': project, 'type': 'Project'})