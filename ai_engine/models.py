from django.db import models
from django.contrib.auth.models import User

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