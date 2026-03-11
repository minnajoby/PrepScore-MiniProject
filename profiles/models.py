# In profiles/models.py

from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255, default='images/avatar1.jpg')
    location = models.CharField(max_length=255, blank=True)
    resume_pdf = models.FileField(upload_to='resumes/', null=True, blank=True)

    # Professional Data (Extracted from Resume)
    resume_text = models.TextField(blank=True)
    from pgvector.django import VectorField
    resume_embedding = VectorField(dimensions=768, null=True, blank=True)

    # AI Engine Features
    num_projects = models.IntegerField(default=0)
    num_skills = models.IntegerField(default=0)
    num_experiences = models.IntegerField(default=0)
    num_educations = models.IntegerField(default=0)
    num_certifications = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

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
    issuing_organization = models.CharField(max_length=200, blank=True)
    date_issued = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    date_graduated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} at {self.school}"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=500, blank=True)
    technologies_used = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title