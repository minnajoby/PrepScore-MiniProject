from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Skill, Experience, Certification, Education, Project

@receiver([post_save, post_delete], sender=Project)
def update_project_count(sender, instance, **kwargs):
    profile = instance.profile
    profile.num_projects = Project.objects.filter(profile=profile).count()
    profile.save(update_fields=['num_projects'])

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

@receiver([post_save, post_delete], sender=Education)
def update_education_count(sender, instance, **kwargs):
    profile = instance.profile
    profile.num_educations = Education.objects.filter(profile=profile).count()
    profile.save(update_fields=['num_educations'])
