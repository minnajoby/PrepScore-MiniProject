from django.contrib import admin
from .models import Profile, Skill, Experience, Certification

# This tells the admin site to create an interface for each of your models.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Certification)