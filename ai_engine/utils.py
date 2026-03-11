import fitz
import numpy as np
from google import genai
from django.conf import settings

def extract_text_from_pdf(pdf_path):
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
    if not text:
        return None
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        result = client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=text,
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def compute_similarity(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return 0.0
    
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Zero vector check
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
        
    cosine_sim = np.dot(vec1, vec2) / (norm1 * norm2)
    return float(cosine_sim)