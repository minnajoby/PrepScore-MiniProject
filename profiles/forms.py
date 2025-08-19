# In profiles/forms.py

from django import forms
from .models import Skill,Education,Experience# Import the Skill model

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        # Specify which fields from the model should be in the form
        fields = ['name'] 
        # We don't include 'profile' here because we will set it automatically in the view

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        # We want fields for degree, institution, and year of completion
        fields = ['degree', 'institution', 'year_of_completion']
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        # Specify the fields you want the user to fill out
        fields = ['title', 'company', 'description']
