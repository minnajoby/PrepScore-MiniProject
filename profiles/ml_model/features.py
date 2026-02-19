# In profiles/ml_model/features.py

import pandas as pd

# Import your models (used to get counts)
from profiles.models import Profile, Skill, Experience, Certification

# --- THIS IS THE KEY CHANGE ---
# Import the shared keyword configuration from your new central config file.
from profiles.config import SKILL_SCORES

# Get the list of all special keywords we're tracking
TRACKED_KEYWORDS = SKILL_SCORES.keys()


# --- DEFINITIVE FEATURE ORDER ---
# This list defines the exact order of columns that your Machine Learning model
# was trained on. It is CRUCIAL that the live feature vector matches this order.
MODEL_FEATURES = [
    'num_projects',
    'num_experiences',
    'num_skills',
    'num_educations',
    'num_certifications',
]

# --- THE FEATURE ENGINEERING FUNCTION ---
def profile_to_vector(profile):
    """
    Converts a live user profile object into a feature vector (a single-row
    pandas DataFrame) with a guaranteed column order for the ML model.
    """
    
    # --- Step 1: Calculate all the raw values from the profile ---
    # Now we read the cached/manual values from the Profile model itself
    num_projects = profile.num_projects
    num_experiences = profile.num_experiences
    num_skills = profile.num_skills
    num_educations = profile.num_educations
    num_certifications = profile.num_certifications

    # --- Step 2: Build the list of feature values in the CORRECT order ---
    # This order must match the MODEL_FEATURES list defined above.
    feature_values = [
        num_projects,
        num_experiences,
        num_skills,
        num_educations,
        num_certifications,
    ]

    # --- Step 3: Create the final DataFrame ---
    live_df = pd.DataFrame([feature_values], columns=MODEL_FEATURES)
    
    return live_df