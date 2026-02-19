import os
import django
import random
import pandas as pd
import numpy as np
from faker import Faker

# Setup Django environment (though we might not need models directly for this purely synthetic generation, 
# it's good practice in case we want to cross-reference config)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepscore_project.settings')
django.setup()

# Import shared configuration
from profiles.config import SKILL_SCORES

fake = Faker()

def generate_rigorous_data(num_records=2000):
    print(f"--- Starting Rigorous Data Generation for {num_records} students ---")
    
    data = []
    
    # Get the list of tracked technical skills (filtering out soft skills for the count)
    # We'll use the config to identify tech skills vs soft skills
    all_skills = list(SKILL_SCORES.keys())
    # A simple heuristic: if it's in the 'soft' list, it's soft.
    # From config.py: project management, communication, leadership, problem solving
    soft_skills_list = ['project management', 'communication', 'leadership', 'problem solving']
    tech_skills_list = [s for s in all_skills if s not in soft_skills_list]
    
    print("Applying Strict Scoring Logic:")
    print("1. Base Score = GPA * 5")
    print("2. Internship Boost = 2 * Internship Months")
    print("3. Project Boost = 10 * Num Complex Projects")
    print("4. Hackathon Bonus = +15 if win")
    print("5. Cap at 100")

    for _ in range(num_records):
        # --- 1. Generate Realistic Features ---
        
        # GPA: 6.0 to 10.0 (Weighted towards 7.5 - 9.0)
        gpa = round(random.triangular(6.0, 10.0, 8.0), 1)
        
        # Internship Months: 0 to 24
        # Skewed towards 0-6 months
        internship_months = np.random.choice(
            list(range(0, 25)), 
            p=[0.4] + [0.6/24]*24 # 40% have 0 months, rest distributed
        )
        # Fix probability sum to exactly 1.0 just in case
        internship_months = int(internship_months) # Ensure int
        
        # Complex Projects: 0 to 5
        # Weighted: 0 (20%), 1 (40%), 2 (25%), 3 (10%), 4 (4%), 5 (1%)
        num_complex_projects = np.random.choice(
            [0, 1, 2, 3, 4, 5],
            p=[0.2, 0.4, 0.25, 0.1, 0.04, 0.01]
        )
        
        # Hackathon Wins: 0 or 1
        # Rare event (5% chance)
        hackathon_wins = 1 if random.random() < 0.05 else 0
        
        # Skill Count (Technical): 1 to 15
        skill_count = int(np.random.normal(5, 3))
        skill_count = max(1, min(skill_count, len(tech_skills_list)))
        
        # Soft Skill Score: 1 to 10
        # Correlated slightly with GPA? Let's keep it independent but normally distributed high
        soft_skill_score = int(np.random.normal(7, 2))
        soft_skill_score = max(1, min(soft_skill_score, 10))
        
        
        # --- 2. Calculate Target Score (Readiness) ---
        
        score = 0
        
        # Base: GPA * 5
        score += gpa * 5
        
        # Internship: 2 points per month
        score += internship_months * 2
        
        # Projects: 10 points per complex project
        score += num_complex_projects * 10
        
        # Hackathon: Flat +15 bonus
        if hackathon_wins == 1:
            score += 15
            
        # Cap at 100, Floor at 0
        readiness_score = max(0, min(int(score), 100))
        
        
        # --- 3. Construct Row ---
        row = {
            'internship_months': internship_months,
            'num_complex_projects': num_complex_projects,
            'gpa': gpa,
            'hackathon_wins': hackathon_wins,
            'skill_count': skill_count,
            'soft_skill_score': soft_skill_score,
            'readiness_score': readiness_score
        }
        
        data.append(row)
        
    # --- 4. Export to CSV ---
    df = pd.DataFrame(data)
    
    # Ensure column order matches user request EXACTLY
    expected_cols = [
        'internship_months', 'num_complex_projects', 'gpa', 
        'hackathon_wins', 'skill_count', 'soft_skill_score', 
        'readiness_score'
    ]
    df = df[expected_cols]
    
    output_filename = 'training_data_final.csv'
    df.to_csv(output_filename, index=False)
    
    print(f"\n--- Success! Generated {len(df)} rows in '{output_filename}' ---")
    print("\nPreview of the first 5 rows:")
    print(df.head())

if __name__ == "__main__":
    generate_rigorous_data()
