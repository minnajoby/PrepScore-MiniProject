# In profiles/models.py

from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255, default='images/avatar1.jpg')
    location = models.CharField(max_length=255, blank=True)
    resume_pdf = models.FileField(upload_to='resumes/', null=True, blank=True)

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

# --- SIGNALS FOR AUTO-UPDATING PROFILE COUNTS ---
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Skill)
def update_skill_count(sender, instance, **kwargs):
    profile = instance.profile
    profile.num_skills = Skill.objects.filter(profile=profile).count()
    profile.save(update_fields=['num_skills'])

@receiver([post_save, post_delete], sender=Experience)
def update_experience_count(sender, instance, **kwargs):
    profile = instance.profile
    profile.num_experiences = Experience.objects.filter(profile=profile).count()
    profile.save(update_fields=['num_experiences'])

@receiver([post_save, post_delete], sender=Certification)
def update_certification_count(sender, instance, **kwargs):
    profile = instance.profile
    profile.num_certifications = Certification.objects.filter(profile=profile).count()
    profile.save(update_fields=['num_certifications'])