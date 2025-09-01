# In profiles/scorer.py
from .models import Skill, Education, Experience, Certification

def calculate_prep_score(profile):
    """
    Calculates a career readiness score based on a user's profile.
    This version now includes points for LinkedIn and GitHub profiles.
    """
    if not profile:
        return 0

    # --- Define the points for each item ---
    POINTS_PER_SKILL = 5
    POINTS_PER_EDUCATION = 15
    POINTS_PER_EXPERIENCE = 20
    POINTS_PER_CERTIFICATION = 10
    
    # --- NEW: Define points for professional links ---
    POINTS_FOR_LINKEDIN = 10
    POINTS_FOR_GITHUB = 10

    # --- Get the counts of each item for the given profile ---
    num_skills = Skill.objects.filter(profile=profile).count()
    num_educations = Education.objects.filter(profile=profile).count()
    num_experiences = Experience.objects.filter(profile=profile).count()
    num_certifications = Certification.objects.filter(profile=profile).count()

    # --- Calculate the base score ---
    score = (
        (num_skills * POINTS_PER_SKILL) +
        (num_educations * POINTS_PER_EDUCATION) +
        (num_experiences * POINTS_PER_EXPERIENCE) +
        (num_certifications * POINTS_PER_CERTIFICATION)
    )
    
    # --- NEW: Add points for professional links if they exist ---
    # We check if the field is not empty or None
    if profile.linkedin_url:
        score += POINTS_FOR_LINKEDIN
    
    if profile.github_url:
        score += POINTS_FOR_GITHUB
        
    return score