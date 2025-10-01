# In profiles/config.py

# This single dictionary now holds the score for every recognized skill.
# High-value skills get more points. All other skills will get a default score.
SKILL_SCORES = {
    # High-Value Tech Skills
    'machine learning': 15,
    'data analysis': 12,
    'aws': 10,
    'azure': 10,
    'gcp': 10,
    'python': 10,
    'django': 8,
    'react': 8,
    'javascript': 7,
    'sql': 8,
    'git': 7,
    
    # Important Soft/Business Skills
    'project management': 10,
    'communication': 5,
    'leadership': 6,
    'problem solving': 5,
}

# Any skill NOT in the dictionary above will receive this default score.
DEFAULT_SKILL_SCORE = 3

# Points for other profile sections remain the same
BASE_POINTS = {
    'education': 20,
    'experience': 25,
    'certification': 15,
    'linkedin': 10,
    'github': 10,
    'bio': 5,
}