# In generate_data.py
import os
import django
import random
from faker import Faker

# --- SETUP DJANGO ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepscore_project.settings')
django.setup()

from django.contrib.auth.models import User
from profiles.models import Profile, Skill, Education, Experience, Certification

fake = Faker()

# --- EXPANDED DATA CONFIGURATION ---
SKILL_CHOICES = [
    'Python', 'JavaScript', 'React', 'Django', 'SQL', 'PostgreSQL', 'AWS', 'Azure', 'Docker',
    'Git', 'Project Management', 'Communication', 'Teamwork', 'Data Analysis', 'Machine Learning',
    'HTML', 'CSS', 'REST APIs', 'Agile Methodologies', 'Scrum', 'Java', 'C++', 'Public Speaking',
    'Node.js', 'TypeScript', 'Vue.js', 'Angular', 'MongoDB', 'Firebase', 'Kubernetes', 'Terraform',
    'Problem Solving', 'Critical Thinking', 'Leadership', 'Adaptability', 'Creativity', 'UI/UX Design',
    'Figma', 'Adobe XD', 'SEO', 'Content Marketing', 'Google Analytics', 'Tableau', 'Power BI'
]
TECH_SKILLS = {'Python', 'JavaScript', 'React', 'Django', 'SQL', 'PostgreSQL', 'AWS', 'Azure', 'Docker', 'Git', 'Java', 'C++', 'Node.js', 'TypeScript', 'Vue.js', 'Angular', 'MongoDB', 'Firebase', 'Kubernetes', 'Terraform'}
SOFT_SKILLS = {'Project Management', 'Communication', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Leadership', 'Adaptability', 'Creativity'}

DEGREE_CHOICES = ['B.Sc. Computer Science', 'B.Tech IT', 'MCA', 'M.Sc. Data Science', 'B.A. Economics', 'B.Com Finance', 'BBA Marketing', 'M.Tech Software Engineering']
JOB_TITLES = ['Software Engineer Intern', 'Junior Web Developer', 'Data Analyst Trainee', 'Cloud Intern', 'Marketing Intern', 'Product Management Intern']

def create_profile(profile_type):
    """Creates a user profile based on a specific type, ensuring a unique username."""
    
    # --- THIS IS THE FIX: A LOOP TO GUARANTEE A UNIQUE USERNAME ---
    while True:
        first_name = fake.first_name()
        last_name = fake.last_name()
        random_num = random.randint(100, 9999)
        username = f'{first_name.lower()}.{last_name.lower()}{random_num}'
        
        # Check the database to see if this username already exists
        if not User.objects.filter(username=username).exists():
            # If it's unique, we can exit the loop
            break
    # --- END OF FIX ---
    
    email = f'{username}@example.com'
    user = User.objects.create_user(username=username, email=email, password='password123')
    profile = Profile.objects.create(user=user)
    
    # --- Profile Type Logic ---
    if profile_type == 'empty':
        pass

    elif profile_type == 'weak':
        profile.headline = "Student"
        Skill.objects.create(profile=profile, name=random.choice(list(TECH_SKILLS)))
        Education.objects.create(profile=profile, degree=random.choice(DEGREE_CHOICES), institution=fake.company()+" College", year_of_completion=2024)

    elif profile_type == 'average':
        profile.headline = fake.catch_phrase()
        profile.bio = fake.paragraph(nb_sentences=3)
        profile.location = fake.city()
        if random.random() < 0.5: profile.linkedin_url = f'https://linkedin.com/in/{username}'
        for _ in range(random.randint(4, 7)): Skill.objects.create(profile=profile, name=random.choice(SKILL_CHOICES))
        for _ in range(random.randint(1, 2)): Education.objects.create(profile=profile, degree=random.choice(DEGREE_CHOICES), institution=fake.company()+" University", year_of_completion=random.randint(2022, 2025))
        if random.random() < 0.5: Experience.objects.create(profile=profile, title=random.choice(JOB_TITLES), company=fake.company())

    elif profile_type == 'tech_specialist':
        profile.headline = "Backend Developer"
        profile.bio = "Focused on building scalable backend systems."
        profile.github_url = f'https://github.com/{username}'
        for skill_name in random.sample(list(TECH_SKILLS), k=10): Skill.objects.create(profile=profile, name=skill_name)
        Experience.objects.create(profile=profile, title="Software Intern", company=fake.company())

    elif profile_type == 'soft_skill_specialist':
        profile.headline = "Aspiring Project Manager"
        profile.bio = "Passionate about leading teams and delivering projects."
        profile.linkedin_url = f'https://linkedin.com/in/{username}'
        for skill_name in random.sample(list(SOFT_SKILLS), k=6): Skill.objects.create(profile=profile, name=skill_name)
        Experience.objects.create(profile=profile, title="Team Lead (Volunteer)", company="NGO")

    elif profile_type == 'well_rounded':
        profile.headline = f"{random.choice(JOB_TITLES)} | Python | AWS | Project Management"
        profile.bio = fake.paragraph(nb_sentences=6)
        profile.location = f"{fake.city()}, {fake.country()}"
        profile.linkedin_url = f'https://linkedin.com/in/{username}'
        profile.github_url = f'https://github.com/{username}'
        for _ in range(random.randint(8, 12)): Skill.objects.create(profile=profile, name=random.choice(SKILL_CHOICES))
        for _ in range(random.randint(2, 3)): Education.objects.create(profile=profile, degree=random.choice(DEGREE_CHOICES), institution=fake.company()+" University", year_of_completion=random.randint(2020, 2025))
        for _ in range(random.randint(2, 3)): Experience.objects.create(profile=profile, title=random.choice(JOB_TITLES), company=fake.company())
        for _ in range(random.randint(1, 3)): Certification.objects.create(profile=profile, name=f"Certified {random.choice(['AWS', 'Python', 'Agile'])}", issuing_organization=fake.company())
        
    profile.save()
    print(f"Created {profile_type.upper()} User: {username}")

def main(profile_counts):
    """Main function to generate a stratified dataset."""
    print("--- Starting Stratified Data Generation ---")
    User.objects.exclude(is_superuser=True).delete() # Start fresh

    total_created = 0
    for profile_type, count in profile_counts.items():
        print(f"\n--- Creating {count} profiles of type: {profile_type} ---")
        for _ in range(count):
            create_profile(profile_type)
            total_created += 1
            
    print(f"\n--- Successfully created {total_created} new, varied user profiles! ---")

if __name__ == '__main__':
    # --- Define our stratified sample here ---
    PROFILE_COUNTS = {
        'empty': 100,
        'weak': 400,
        'average': 1000,
        'tech_specialist': 200,
        'soft_skill_specialist': 200,
        'well_rounded': 100,
    }
    main(PROFILE_COUNTS)