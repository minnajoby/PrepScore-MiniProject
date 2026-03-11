# In profiles/forms.py

from django import forms
from .models import Profile, Skill, Experience, Certification, Education, Project
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    # We use a generic name 'login' for the field
    login = forms.CharField(label="Username or Email", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # The fields tuple defines the order Django processes them
        fields = ("username", "email", "password1", "password2")

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'description']
        
        # This tells Django to add the 'form-control' class to each field's HTML
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'resume_pdf']
        
        # This is the key. We tell Django what classes to add to the HTML.
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'resume_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        # These are the fields the user will fill out
        fields = ['name', 'issuing_organization', 'date_issued']
        
        # This part is crucial for Bootstrap styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            
            # This tells Django to render the date field as an HTML5 date input
            'date_issued': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field_of_study', 'date_graduated']
        widgets = {
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'date_graduated': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'technologies_used']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. PrepScore Platform'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your role and impact...'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'technologies_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Django, Python, Bootstrap'}),
        }
    