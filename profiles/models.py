# In profiles/models.py

from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255, default='images/avatar1.jpg')
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.user.username

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year_of_completion = models.IntegerField()
    def __str__(self):
        return self.degree

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.title

class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    # --- ADD THESE TWO NEW FIELDS ---
    issuing_organization = models.CharField(max_length=200, blank=True)
    date_issued = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name