# In profiles/scorer.py
import os
import joblib
import random
import numpy as np
from django.conf import settings
from .models import Profile, Skill, Experience, Certification
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
    if profile.resume_pdf: contributions["Profile Details"] += 20 # Bonus for resume?

    # Score other sections
    contributions["Education"] = profile.num_educations * BASE_POINTS['education']
    contributions["Experience"] = profile.num_experiences * BASE_POINTS['experience']
    contributions["Certifications"] = profile.num_certifications * BASE_POINTS['certification']
    contributions["Projects"] = profile.num_projects * BASE_POINTS.get('project', 15)

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
        (2 * BASE_POINTS['certification']) +
        (3 * BASE_POINTS.get('project', 15))
    )
    
    # Get the user's current raw score
    contributions = get_score_contributions(profile)
    current_raw_score = sum(contributions.values())
    
    if MAX_POSSIBLE_SCORE == 0:
        return 0
        
    # --- Calculate the score as a percentage ---
    final_score = round((current_raw_score / MAX_POSSIBLE_SCORE) * 100)
    
    return min(final_score, 100)


# --- 2. THE LIVE ML SCORING ENGINE ---

MODEL_PATH = os.path.join(settings.BASE_DIR, 'profiles', 'ml_models', 'prepscore_model.joblib')
PREPSCORE_MODEL = None

try:
    if os.path.exists(MODEL_PATH):
        PREPSCORE_MODEL = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading ML model: {e}")

def profile_to_vector(profile):
    """
    Extracts numerical features from a Profile instance for the ML model.
    Order must match the training script: 
    [num_skills, num_experiences, num_educations, num_certifications, num_projects]
    """
    if not profile:
        return np.zeros((1, 5))
    
    vector = [
        profile.num_skills,
        profile.num_experiences,
        profile.num_educations,
        profile.num_certifications,
        profile.num_projects
    ]
    return np.array(vector).reshape(1, -1)

def calculate_ml_score(profile):
    """
    Calculates the live PrepScore using the ML model.
    """
    if not profile: return 0
    
    # Check if there's any content at all
    has_content = (
        profile.num_skills > 0 or profile.num_educations > 0 or
        profile.num_experiences > 0 or profile.num_certifications > 0 or
        profile.num_projects > 0
    )
    if not has_content: return 0

    if PREPSCORE_MODEL is None: 
        # Fallback to rule-based score if the model isn't trained or loaded yet
        return calculate_rule_based_score(profile)

    try:
        feature_vector = profile_to_vector(profile)
        predicted_score = PREPSCORE_MODEL.predict(feature_vector)[0]
        
        # Use standard rounding
        final_score = round(float(predicted_score))
        return max(0, min(final_score, 100))
    except Exception as e:
        print(f"Error during ML prediction: {e}")
        return calculate_rule_based_score(profile)


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
    if profile.num_projects == 0: suggestions.append({ "priority": 1.5, "text": "Showcase your practical skills by adding your key technical projects." })
    if profile.num_educations == 0: suggestions.append({ "priority": 3, "text": "Add your academic background to build a more complete profile and boost your score." })
    
    missing_keywords = [k for k in SKILL_SCORES.keys() if k not in skill_names]
    if missing_keywords: suggestions.append({ "priority": 2, "text": f"Consider learning a high-demand skill like '{random.choice(missing_keywords).title()}'." })
    
    if len(skill_names) < 5: suggestions.append({ "priority": 4, "text": "Broaden your skillset. Aim to list at least 5-7 relevant technical and soft skills." })
    
    sorted_suggestions = sorted(suggestions, key=lambda x: x['priority'])
    final_suggestions = [s['text'] for s in sorted_suggestions[:3]]
    
    if not final_suggestions: return ["Your profile is very well-rounded! Consider adding more detail to your project descriptions."]
    return final_suggestions