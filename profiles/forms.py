# In profiles/forms.py

from django import forms
from .models import Profile,Skill,Experience,Certification # Import the Skill model
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
        fields = ['location', 'resume']
        
        # This is the key. We tell Django what classes to add to the HTML.
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
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
    