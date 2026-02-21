from django.urls import path
from . import views

urlpatterns = [
    path('process-resume/', views.process_resume_view, name='process_resume'),
    path('gap-analysis/', views.gap_analysis_view, name='gap_analysis'),
] 
