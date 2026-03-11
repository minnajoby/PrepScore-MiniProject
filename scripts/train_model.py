import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Ensure we can import from the profiles app if needed, 
# but for synthetic data generation we'll just replicate the logic.
BASE_POINTS = {
    'education': 20,
    'experience': 25,
    'certification': 15,
    'project': 15,
    'skill_avg': 5
}

def generate_synthetic_data(num_samples=5000):
    """
    Generates synthetic profile data for training.
    Features: num_skills, num_experiences, num_educations, num_certifications, num_projects
    """
    data = []
    for _ in range(num_samples):
        num_skills = np.random.randint(0, 15)
        num_exp = np.random.randint(0, 8)
        num_edu = np.random.randint(0, 4)
        num_certs = np.random.randint(0, 6)
        num_projs = np.random.randint(0, 6)
        
        # Calculate a "perfect" raw score for normalization
        MAX_RAW = (10 * 5) + (2 * 20) + (3 * 25) + (2 * 15) + (3 * 15) # Consistent with scorer.py
        
        # Calculate raw score for this sample
        raw_score = (
            (num_skills * 5) + 
            (num_edu * 20) + 
            (num_exp * 25) + 
            (num_certs * 15) + 
            (num_projs * 15)
        )
        
        # Target score (percentage)
        target_score = min(round((raw_score / MAX_RAW) * 100), 100)
        
        # Add some noise to make it "ML-worthy"
        noise = np.random.normal(0, 2)
        target_score = max(0, min(100, round(target_score + noise)))
        
        data.append([num_skills, num_exp, num_edu, num_certs, num_projs, target_score])
        
    columns = ['num_skills', 'num_experiences', 'num_educations', 'num_certifications', 'num_projects', 'score']
    return pd.DataFrame(data, columns=columns)

def train_and_save_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df.drop('score', axis=1)
    y = df['score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.4f}")
    
    # Save model
    model_path = os.path.join('profiles', 'ml_models', 'prepscore_model.joblib')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
