from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),  # Login URL
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('skill/add/', views.add_skill_view, name='add_skill'),
    path('education/add/', views.add_education_view, name='add_education'),
    path('experience/add/', views.add_experience_view, name='add_experience'),
    path('skill/<int:pk>/edit/', views.edit_skill_view, name='edit_skill'),

]
