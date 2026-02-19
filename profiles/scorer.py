# In profiles/scorer.py
import os
import joblib
import random
from django.conf import settings

# --- IMPORTS ---
from .models import Profile, Skill, Experience, Certification
from .ml_model.features import profile_to_vector
from .config import SKILL_SCORES, DEFAULT_SKILL_SCORE, BASE_POINTS


# --- 1. THE RULE-BASED SCORING ENGINE (for Data Generation & Charts) ---

def get_score_contributions(profile):
    """
    Calculates the raw points contributed by each profile category using the rule-based system.
    """
    contributions = {
        "Skills": 0, "Education": 0, "Experience": 0,
        "Certifications": 0, "Profile Details": 0
    }
    if not profile:
        return contributions

    # Score Core Profile Details
    # (Bio, Headline, Sites removed for AI optimization)
    if profile.resume: contributions["Profile Details"] += 20 # Bonus for resume?

    # Score other sections
    contributions["Education"] = profile.num_educations * BASE_POINTS['education']
    contributions["Experience"] = profile.num_experiences * BASE_POINTS['experience']
    contributions["Certifications"] = profile.num_certifications * BASE_POINTS['certification']

    # Balanced skill scoring
    for skill in profile.skill_set.all():
        contributions["Skills"] += SKILL_SCORES.get(skill.name.lower(), DEFAULT_SKILL_SCORE)
        
    return contributions

def calculate_rule_based_score(profile):
    """
    Calculates a more realistic, percentage-based score.
    This is the "ground truth" for training the ML model.
    """
    if not profile:
        return 0
    
    # --- Define the score for a "perfect" 100-point profile ---
    # You can adjust these targets if you want to change the scoring weight
    MAX_POSSIBLE_SCORE = (
        (10 * 5) + # Approx. score for 10 skills
        (2 * BASE_POINTS['education']) +
        (3 * BASE_POINTS['experience']) +
        (2 * BASE_POINTS['certification'])
    )
    
    # Get the user's current raw score
    contributions = get_score_contributions(profile)
    current_raw_score = sum(contributions.values())
    
    if MAX_POSSIBLE_SCORE == 0:
        return 0
        
    # --- Calculate the score as a percentage ---
    final_score = round((current_raw_score / MAX_POSSIBLE_SCORE) * 100)
    
    return min(final_score, 100)


# --- 2. THE LIVE MACHINE LEARNING SCORER ---

try:
    model_path = os.path.join(settings.BASE_DIR, 'profiles', 'ml_model', 'prepscore_ml_model.pkl')
    PREPSCORE_MODEL = joblib.load(model_path)
    print("--- Machine Learning model loaded successfully! ---")
except FileNotFoundError:
    PREPSCORE_MODEL = None
    print("--- WARNING: Machine Learning model file not found. Live scoring will default to 0. ---")

def calculate_ml_score(profile):
    """
    Calculates the live PrepScore using the ML model.
    """
    if not profile: return 0
    
    has_content = (
        profile.num_skills > 0 or profile.num_educations > 0 or
        profile.num_experiences > 0 or profile.num_certifications > 0
    )
    if not has_content: return 0
    if PREPSCORE_MODEL is None: return 0

    feature_vector = profile_to_vector(profile)
    predicted_score = PREPSCORE_MODEL.predict(feature_vector)[0]
    
    # Use standard rounding, not int()
    final_score = round(predicted_score)
    
    return max(0, min(final_score, 100)) # Ensure score is between 0 and 100


# --- 3. THE RECOMMENDATION & ANALYSIS ENGINES ---

def get_suggestions(profile, score):
    """Analyzes profile and score to return prioritized, actionable suggestions."""
    if score >= 95:
        return ["Your profile is outstanding! Keep it updated with your latest achievements."]
    if not profile: return ["Start by building your profile! Add your skills, education, and any experience you have."]
    
    suggestions = []
    num_experiences = profile.num_experiences
    skill_names = {skill.name.lower() for skill in Skill.objects.filter(profile=profile)}
    
    if num_experiences == 0: suggestions.append({ "priority": 1, "text": "Gaining practical experience through an internship or personal project is the most impactful way to boost your score." })
    
    missing_keywords = [k for k in SKILL_SCORES.keys() if k not in skill_names]
    if missing_keywords: suggestions.append({ "priority": 2, "text": f"Consider learning a high-demand skill like '{random.choice(missing_keywords).title()}'." })
    
    if len(skill_names) < 5: suggestions.append({ "priority": 4, "text": "Broaden your skillset. Aim to list at least 5-7 relevant technical and soft skills." })
    
    sorted_suggestions = sorted(suggestions, key=lambda x: x['priority'])
    final_suggestions = [s['text'] for s in sorted_suggestions[:3]]
    
    if not final_suggestions: return ["Your profile is very well-rounded! Consider adding more detail to your project descriptions."]
    return final_suggestions