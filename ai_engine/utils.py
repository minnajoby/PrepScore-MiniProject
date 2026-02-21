import fitz  # PyMuPDF
import numpy as np
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text.strip()

def generate_embedding(text):
    """
    Generate a 768-dimension embedding vector using Gemini API.
    Free, runs on Google's servers — no RAM issues on deployment.
    """
    if not text:
        return None
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def compute_similarity(embedding1, embedding2):
    """Cosine similarity between two vectors. Returns 0.0 to 1.0."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    cosine_sim = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
    return float(cosine_sim)