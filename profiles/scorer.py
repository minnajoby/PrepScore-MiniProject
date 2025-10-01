# In profiles/scorer.py
import os
import joblib
from django.conf import settings

# --- THIS IS THE FIX ---
# We must import all the models that the recommendation engine uses.
from .models import Profile, Skill, Education, Experience, Certification

# Import the feature engineering pipeline
from .ml_model.features import profile_to_vector

# Import the shared keyword configuration
from .config import SKILL_SCORES,DEFAULT_SKILL_SCORE,BASE_POINTS

# --- LOAD THE TRAINED MACHINE LEARNING MODEL ---
try:
    model_path = os.path.join(settings.BASE_DIR, 'profiles', 'ml_model', 'prepscore_ml_model.pkl')
    PREPSCORE_MODEL = joblib.load(model_path)
    print("--- Machine Learning model loaded successfully! ---")
except FileNotFoundError:
    PREPSCORE_MODEL = None
    print("--- WARNING: Machine Learning model file not found. Scoring will default to 0. ---")


# --- THE HYBRID SCORING FUNCTION (ML + RULES) ---
def calculate_ml_score(profile):
    # ... (This function remains the same as before) ...
    if not profile: return 0
    has_content = (
        profile.skill_set.exists() or profile.education_set.exists() or
        profile.experience_set.exists() or profile.certification_set.exists() or
        profile.bio or profile.headline
    )
    if not has_content: return 0
    if PREPSCORE_MODEL is None: return 0
    feature_vector = profile_to_vector(profile)
    predicted_score = PREPSCORE_MODEL.predict(feature_vector)[0]
    final_score = round(predicted_score)
    if has_content and final_score < 5: return 5
    return max(0, min(final_score, 100))


# --- NEW, ML-ALIGNED RECOMMENDATION FUNCTION ---
def get_suggestions(profile, score):
    """
    Analyzes a user's profile and score to return prioritized, actionable suggestions
    that align with the features the ML model was trained on.
    """
    if score >= 95:
        return [
            "Your profile is outstanding! You've achieved a top-tier PrepScore.",
            "Focus on keeping your experience descriptions updated with your latest achievements."
        ]

    if not profile:
        return ["Start by building your profile! Add your skills, education, and any experience you have."]

    suggestions = []
    
    # Get profile data for analysis
    num_experiences = profile.experience_set.count()
    skill_names = {skill.name.lower() for skill in Skill.objects.filter(profile=profile)}

    # --- Prioritized Recommendations based on Model Features ---
    # PRIORITY 1: Experience
    if num_experiences == 0:
        suggestions.append({ "priority": 1, "text": "The most impactful way to boost your score is by gaining practical experience. Seek an internship or start a significant personal project." })
    elif num_experiences < 2:
        suggestions.append({ "priority": 2, "text": "You have some experience, which is great! Adding another project or internship will make your profile much stronger." })

    # PRIORITY 2: High-Value Skills
    missing_keywords = [k for k in SKILL_SCORES.keys() if k not in skill_names]
    if missing_keywords:
        suggestions.append({ "priority": 2, "text": f"Consider learning a high-demand skill like '{missing_keywords[0].title()}'. It provides a significant score boost." })

    # PRIORITY 3: Core Profile Completeness
    if not profile.bio or len(profile.bio) < 100:
        suggestions.append({ "priority": 3, "text": "Expand on your professional bio. A detailed summary of 100+ characters helps recruiters and improves your score." })
    if hasattr(profile, 'github_url') and not profile.github_url:
         suggestions.append({ "priority": 3, "text": "Your GitHub profile is a portfolio of your coding skills. Add the URL to your profile." })

    # PRIORITY 4: General Skill Quantity
    if len(skill_names) < 5:
        suggestions.append({ "priority": 4, "text": "Broaden your skillset. Aim to list at least 5-7 relevant technical and soft skills." })
    
    # --- Final Logic ---
    sorted_suggestions = sorted(suggestions, key=lambda x: x['priority'])
    final_suggestions = [s['text'] for s in sorted_suggestions[:3]]

    if not final_suggestions:
        return ["Your profile is very well-rounded! No critical gaps were found. Consider adding more detail to your project descriptions."]

    return final_suggestions

def get_strong_areas(profile):
    """Identifies the top strengths of a user's profile."""
    if not profile: return []
    
    strengths = []
    if profile.experience_set.exists():
        strengths.append("Practical Work Experience")
    
    # Check for a good number of high-value skills
    skill_names = {skill.name.lower() for skill in profile.skill_set.all()}
    high_value_skills = [s for s in skill_names if s in SKILL_SCORES and SKILL_SCORES[s] >= 10]
    if len(high_value_skills) >= 3:
        strengths.append(f"Expertise in High-Demand Skills (like {', '.join(high_value_skills).title()})")

    if profile.certification_set.exists():
        strengths.append("Professional Certifications")
        
    if not strengths:
        return ["Profile is still developing."]
        
    return strengths

# --- AND ADD THIS NEW FUNCTION ---
def get_weak_areas(profile):
    """Identifies the key areas for improvement in a user's profile."""
    if not profile: return []

    weaknesses = []
    if not profile.experience_set.exists():
        weaknesses.append("Lack of Practical Experience")
        
    if profile.skill_set.count() < 5:
        weaknesses.append("Limited Number of Listed Skills")

    if not hasattr(profile, 'github_url') or not profile.github_url:
        weaknesses.append("Missing GitHub Profile to Showcase Projects")
        
    if not weaknesses:
        return ["No significant weak areas found!"]
        
    return weaknesses
def get_score_contributions(profile):
    """
    Calculates the points contributed by each profile category.
    Returns a dictionary suitable for a chart.
    """
    contributions = {
        "Skills": 0,
        "Education": 0,
        "Experience": 0,
        "Certifications": 0,
        "Profile Details": 0, # For Bio, URLs, etc.
    }

    if not profile:
        return contributions

    # 1. Score Core Profile Details
    if profile.bio: contributions["Profile Details"] += BASE_POINTS['bio']
    if hasattr(profile, 'linkedin_url') and profile.linkedin_url: contributions["Profile Details"] += BASE_POINTS['linkedin']
    if hasattr(profile, 'github_url') and profile.github_url: contributions["Profile Details"] += BASE_POINTS['github']

    # 2. Score other sections based on the rule-based scorer
    contributions["Education"] = Education.objects.filter(profile=profile).count() * BASE_POINTS['education']
    contributions["Experience"] = Experience.objects.filter(profile=profile).count() * BASE_POINTS['experience']
    contributions["Certifications"] = Certification.objects.filter(profile=profile).count() * BASE_POINTS['certification']

    # 3. Score Skills using the detailed logic
    skills = Skill.objects.filter(profile=profile)
    for skill in skills:
        skill_name = skill.name.lower()
        contributions["Skills"] += SKILL_SCORES.get(skill_name, DEFAULT_SKILL_SCORE)
        
    return contributions