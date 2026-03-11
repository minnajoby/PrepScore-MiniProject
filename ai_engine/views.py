import json
from groq import Groq
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import Profile
from profiles.scorer import calculate_ml_score
from .models import GapAnalysisResult
from .utils import extract_text_from_pdf, generate_embedding, compute_similarity



@login_required
def gap_analysis_view(request):
    result = None
    past_results = GapAnalysisResult.objects.filter(user=request.user)[:3]

    profile, _ = Profile.objects.get_or_create(user=request.user)
    resume_ready = bool(profile.resume_text)

    if request.method == 'POST':
        job_description = request.POST.get('job_description', '').strip()

        if not job_description:
            messages.error(request, "Please paste a Job Description.")
            return redirect('gap_analysis')

        if not resume_ready:
            messages.error(request, "Please upload your resume in the Profile section first.")
            return redirect('manage_profile')

        profile = Profile.objects.get(user=request.user)
        rf_score = calculate_ml_score(profile)

        jd_embedding = generate_embedding(job_description[:8000])
        
        if not jd_embedding:
            messages.error(request, "AI was unable to generate an embedding for that Job Description. Please try again.")
            return redirect('gap_analysis')

        similarity = compute_similarity(profile.resume_embedding, jd_embedding)
        vector_score = similarity * 100

        final_score = round((rf_score * 0.6) + (vector_score * 0.4))

        prompt = f"""
You are a Senior Hiring Manager reviewing a candidate's resume against a Job Description.

CANDIDATE RESUME:
{profile.resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Respond ONLY in this exact JSON format, no extra text outside the JSON:
{{
    "missing_skills": ["skill1", "skill2", "skill3"],
    "interview_questions": [
        "Interview question 1 targeting their weak area?",
        "Interview question 2 targeting their weak area?"
    ],
    "summary": "One sentence summary of how well this candidate fits the role."
}}
"""
        try:
            groq_client = Groq(api_key=settings.GROQ_API_KEY)
            chat_response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            response_text = chat_response.choices[0].message.content.strip()

            # Clean markdown JSON wrappers if present
            if response_text.startswith("```"):
                # Remove leading ```json or ``` and trailing ```
                import re
                response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)

            ai_data = json.loads(response_text)

            # --- Aggressive String Cleaning ---
            def clean_text(text):
                if not isinstance(text, str): return text
                # Remove backticks and simple markdown
                import re
                t = re.sub(r'[`*]', '', text) 
                return t.strip()

            clean_skills = [clean_text(s) for s in ai_data.get('missing_skills', [])]
            clean_questions = [clean_text(q) for q in ai_data.get('interview_questions', [])]
            clean_summary = clean_text(ai_data.get('summary', ''))

            GapAnalysisResult.objects.create(
                user=request.user,
                job_description=job_description,
                match_score=final_score,
                missing_skills=clean_skills,
                interview_questions=clean_questions,
                summary=clean_summary,
            )

            result = {
                'rf_score': rf_score,
                'vector_score': round(vector_score),
                'match_score': final_score,
                'missing_skills': clean_skills,
                'interview_questions': clean_questions,
                'summary': clean_summary,
            }

            # Refresh history to include the latest clean result
            past_results = GapAnalysisResult.objects.filter(user=request.user)[:3]

        except Exception as e:
            messages.error(request, f"AI Analysis failed: {str(e)}")

    # Convert to robust dict list - immune to formatter line splits
    history_list = []
    for r in past_results:
        history_list.append({
            'date': r.created_at.strftime("%b %d"),
            'score': r.match_score,
            'color': 'success' if r.match_score >= 70 else ('warning' if r.match_score >= 50 else 'danger')
        })

    context = {
        'result': result,
        'past_results': history_list,
        'resume_ready': resume_ready,
    }
    return render(request, 'ai_engine/gap_analysis.html', context)