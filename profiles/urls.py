from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('features/', views.features_view, name='features'),
    path('skill/add/', views.add_skill_view, name='add_skill'),
    path('education/add/', views.add_education_view, name='add_education'),
    path('experience/add/', views.add_experience_view, name='add_experience'),
    path('skill/<int:pk>/edit/', views.edit_skill_view, name='edit_skill'),
    path('education/<int:pk>/edit/', views.edit_education_view, name='edit_education'),
    path('experience/<int:pk>/edit/', views.edit_experience_view, name='edit_experience'),
    path('skill/<int:pk>/delete/', views.delete_skill_view, name='delete_skill'),
    path('education/<int:pk>/delete/', views.delete_education_view, name='delete_education'),
    path('experience/<int:pk>/delete/', views.delete_experience_view, name='delete_experience'),
    path('profile/', views.manage_profile_view, name='manage_profile'),
    path('education/', views.manage_education_view, name='manage_education'),
    path('skills/', views.manage_skills_view, name='manage_skills'),
    path('experience/', views.manage_experience_view, name='manage_experience'),
    path('certifications/', views.manage_certifications_view, name='manage_certifications'),
    path('certification/<int:pk>/edit/', views.edit_certification_view, name='edit_certification'),
    path('certification/<int:pk>/delete/', views.delete_certification_view, name='delete_certification'),

]
