# In profiles/scorer.py
from .models import Profile, Skill, Education, Experience, Certification

# --- CONFIGURATION FOR SCORING ---
# Centralized configuration for easy adjustments.
BASE_POINTS = {
    'skill': 5,
    'education': 20,
    'experience': 25,
    'certification': 15,
    'linkedin': 10,
    'github': 10,
    'bio': 5,
}

# Bonus points for specific, high-value keywords in skills (case-insensitive)
KEYWORD_BONUS_POINTS = {
    'python': 10,
    'django': 8,
    'react': 8,
    'javascript': 7,
    'aws': 10,
    'azure': 10,
    'gcp': 10,
    'machine learning': 15,
    'data analysis': 12,
    'git': 7,
    'sql': 8,
    'project management': 10,
    'communication': 5,
}

# --- ENHANCED SCORING FUNCTION ---
def calculate_prep_score(profile):
    """
    Calculates a more realistic score based on the user's progress
    towards an "ideal" complete profile.
    """
    if not profile:
        return 0

    # --- Define the "Ideal" Profile ---
    # These are the targets a user is aiming for.
    MAX_SCORE_TARGETS = {
        'core_profile_items': 3, # Bio, LinkedIn, GitHub
        'skills': 8,
        'educations': 2,
        'experiences': 3,
        'certifications': 3,
        'keyword_skills': 5, # How many high-value keyword skills we're looking for
    }

    # --- Calculate the Maximum Possible Score ---
    # This is the score a "perfect" user would get.
    total_possible_score = (
        (MAX_SCORE_TARGETS['core_profile_items'] * 10) + # e.g., 10 pts each for bio, linkedin, github
        (MAX_SCORE_TARGETS['skills'] * BASE_POINTS['skill']) +
        (MAX_SCORE_TARGETS['educations'] * BASE_POINTS['education']) +
        (MAX_SCORE_TARGETS['experiences'] * BASE_POINTS['experience']) +
        (MAX_SCORE_TARGETS['certifications'] * BASE_POINTS['certification']) +
        (MAX_SCORE_TARGETS['keyword_skills'] * 10) # e.g., an average of 10 bonus points per keyword
    )

    # --- Calculate the User's Current Score ---
    current_score = 0
    
    # 1. Score Core Profile Completion
    core_items_count = 0
    if profile.bio: core_items_count += 1
    if hasattr(profile, 'linkedin_url') and profile.linkedin_url: core_items_count += 1
    if hasattr(profile, 'github_url') and profile.github_url: core_items_count += 1
    current_score += min(core_items_count, MAX_SCORE_TARGETS['core_profile_items']) * 10

    # 2. Score other sections, but cap the count at the target
    num_skills = Skill.objects.filter(profile=profile).count()
    current_score += min(num_skills, MAX_SCORE_TARGETS['skills']) * BASE_POINTS['skill']

    num_educations = Education.objects.filter(profile=profile).count()
    current_score += min(num_educations, MAX_SCORE_TARGETS['educations']) * BASE_POINTS['education']

    num_experiences = Experience.objects.filter(profile=profile).count()
    current_score += min(num_experiences, MAX_SCORE_TARGETS['experiences']) * BASE_POINTS['experience']

    num_certifications = Certification.objects.filter(profile=profile).count()
    current_score += min(num_certifications, MAX_SCORE_TARGETS['certifications']) * BASE_POINTS['certification']

    # 3. Score Keyword Bonuses, capped at the target
    skill_names = [skill.name.lower() for skill in Skill.objects.filter(profile=profile)]
    keyword_count = 0
    for skill_name in skill_names:
        if skill_name in KEYWORD_BONUS_POINTS:
            keyword_count += 1
            current_score += 10 # Add a flat 10 points for each bonus keyword found
    
    # --- Calculate the Final Percentage Score ---
    if total_possible_score == 0:
        return 0 # Avoid division by zero
    
    # Calculate the score as a percentage and round it to a whole number
    final_score = round((current_score / total_possible_score) * 100)
    
    return min(final_score, 100) # Ensure it never goes over 100

# --- ENHANCED RECOMMENDATION FUNCTION (SCORE-AWARE) ---
def get_suggestions(profile, score):
    """
    Analyzes a user's profile and score to return a list of personalized suggestions.
    """
    # Rule 0: If the score is perfect, only give positive feedback.
    if score >= 100:
        return [
            "Congratulations on achieving a perfect PrepScore of 100!",
            "Your profile is outstanding. Keep it updated with your latest achievements."
        ]

    if not profile:
        return ["Start by building your profile! Add your skills, education, and any experience you have."]

    suggestions = []
    
    # Get data for analysis
    skill_names = {skill.name.lower() for skill in Skill.objects.filter(profile=profile)}
    num_experiences = Experience.objects.filter(profile=profile).count()

    # --- Rule-Based Logic for Suggestions ---

    # Rule 1: Check for a professional headline
    if not profile.headline:
        suggestions.append("Create a professional headline. A short, impactful tagline makes a great first impression.")

    # Rule 2: Check for a detailed bio
    if not profile.bio or len(profile.bio) < 100:
        suggestions.append("Expand on your bio. A detailed professional summary helps recruiters understand your goals.")

    # Rule 3: Check for lack of practical experience
    if num_experiences == 0:
        suggestions.append("Practical experience is crucial. Consider seeking an internship or starting a personal project on GitHub.")

    # Rule 4: Suggest foundational tech skills if missing
    if 'git' not in skill_names:
        suggestions.append("Version control is essential. Learning 'Git' is a critical skill for almost every technical role.")
    if 'sql' not in skill_names:
        suggestions.append("Data is everywhere. Learning 'SQL' is a high-demand skill for many roles.")

    # Rule 5 (Contextual): Suggest cloud skills for developers
    web_dev_skills = {'python', 'django', 'javascript', 'react'}
    if any(skill in skill_names for skill in web_dev_skills) and not any(skill in skill_names for skill in ['aws', 'azure', 'gcp']):
        suggestions.append("You have web development skills! Consider learning a cloud platform like 'AWS' or 'Azure'.")
    
    # Rule 6: Check for professional links
    if hasattr(profile, 'linkedin_url') and not profile.linkedin_url:
         suggestions.append("Add your LinkedIn profile URL. It's a key part of your professional online presence.")
    if hasattr(profile, 'github_url') and not profile.github_url:
         suggestions.append("Add your GitHub profile URL to showcase your projects and coding skills.")

    # Rule 7: Final positive reinforcement if other suggestions were found
    if suggestions and len(suggestions) < 3:
         suggestions.append("Your profile is looking good! Addressing these few points will make it even stronger.")

    # Rule 8: Fallback positive message if no gaps were found (but score is not 100)
    if not suggestions:
        suggestions.append("Your profile is very well-rounded! Consider adding more detail to your experience descriptions to maximize your score.")

    return suggestions