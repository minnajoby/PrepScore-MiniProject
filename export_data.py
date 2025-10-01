# In export_data.py

import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepscore_project.settings')
django.setup()

from django.contrib.auth.models import User
# --- IMPORT THE LIVE FEATURE ENGINEERING FUNCTION AND LIST ---
from profiles.ml_model.features import profile_to_vector, MODEL_FEATURES
from profiles.scorer import calculate_rule_based_score

def main():
    print("--- Starting Data Export ---")
    users = User.objects.filter(is_superuser=False)
    all_profiles_data = []

    for user in users:
        if hasattr(user, 'profile'):
            profile = user.profile
            
            # --- USE THE LIVE FUNCTION TO GET THE FEATURES ---
            # profile_to_vector returns a DataFrame, so we get the first row of values
            features_df = profile_to_vector(profile)
            features_dict = features_df.to_dict('records')[0]
            
            # Calculate the score using the old rule-based system
            score = calculate_rule_based_score(profile)
            features_dict['target_score'] = score
            
            all_profiles_data.append(features_dict)

    # --- USE THE IMPORTED LIST FOR THE FINAL DATAFRAME ---
    # We add 'target_score' to the list of columns
    final_columns = MODEL_FEATURES + ['target_score']
    df = pd.DataFrame(all_profiles_data, columns=final_columns)
    
    df.to_csv('training_data.csv', index=False)
    print(f"--- Successfully exported data for {len(all_profiles_data)} profiles to training_data.csv! ---")

if __name__ == '__main__':
    main()