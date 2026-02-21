from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField

class ResumeAnalysis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extracted_text = models.TextField(blank=True)
    embedding = VectorField(dimensions=768, null=True, blank=True)
    last_analyzed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume Analysis — {self.user.username}"


class GapAnalysisResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField()
    match_score = models.IntegerField(default=0)
    missing_skills = models.JSONField(default=list)
    interview_questions = models.JSONField(default=list)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Gap Analysis — {self.user.username} ({self.created_at.date()})"