# In profiles/ml_model/features.py

import pandas as pd

# Import your models (used to get counts)
from profiles.models import Profile, Skill, Education, Experience, Certification

# --- THIS IS THE KEY CHANGE ---
# Import the shared keyword configuration from your new central config file.
from profiles.config import SKILL_SCORES

# Get the list of all special keywords we're tracking
TRACKED_KEYWORDS = SKILL_SCORES.keys()


# --- DEFINITIVE FEATURE ORDER ---
# This list defines the exact order of columns that your Machine Learning model
# was trained on. It is CRUCIAL that the live feature vector matches this order.
MODEL_FEATURES = [
    'num_skills',
    'num_educations',
    'num_experiences',
    'num_certifications',
    'has_bio',
    'has_headline',
    'has_linkedin',
    'has_github'
]
# Add all the keyword skill features to the list in a consistent, sorted order
for keyword in sorted(TRACKED_KEYWORDS):
    MODEL_FEATURES.append(f'has_skill_{keyword.replace(" ", "_")}')


# --- THE FEATURE ENGINEERING FUNCTION ---
def profile_to_vector(profile):
    """
    Converts a live user profile object into a feature vector (a single-row
    pandas DataFrame) with a guaranteed column order for the ML model.
    """
    
    # --- Step 1: Calculate all the raw values from the profile ---
    num_skills = profile.skill_set.count()
    num_educations = profile.education_set.count()
    num_experiences = profile.experience_set.count()
    num_certifications = profile.certification_set.count()

    has_bio = 1 if profile.bio else 0
    has_headline = 1 if profile.headline else 0
    has_linkedin = 1 if hasattr(profile, 'linkedin_url') and profile.linkedin_url else 0
    has_github = 1 if hasattr(profile, 'github_url') and profile.github_url else 0
    
    skill_names = {skill.name.lower() for skill in profile.skill_set.all()}

    # --- Step 2: Build the list of feature values in the CORRECT order ---
    # This order must match the MODEL_FEATURES list defined above.
    feature_values = [
        num_skills,
        num_educations,
        num_experiences,
        num_certifications,
        has_bio,
        has_headline,
        has_linkedin,
        has_github
    ]

    # Add the keyword features in the same sorted order
    for keyword in sorted(TRACKED_KEYWORDS):
        feature_values.append(1 if keyword in skill_names else 0)

    # --- Step 3: Create the final DataFrame ---
    # We wrap feature_values in another list, e.g., [[value1, value2, ...]],
    # to create a single row for the prediction.
    live_df = pd.DataFrame([feature_values], columns=MODEL_FEATURES)
    
    return live_df