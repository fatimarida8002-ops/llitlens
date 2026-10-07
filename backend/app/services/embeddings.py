import json
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_ST_MODEL = None

def get_sentence_transformer_model():
    global _ST_MODEL
    if _ST_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Load lightweight local sentence transformer model
            _ST_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            _ST_MODEL = False
    return _ST_MODEL

def generate_embedding(text: str) -> List[float]:
    """
    Generates dense vector embedding for text.
    """
    model = get_sentence_transformer_model()
    if model:
        try:
            vec = model.encode(text, convert_to_numpy=True)
            return vec.tolist()
        except Exception:
            pass
            
    # TF-IDF fallback vector encoding representation
    words = [w.lower() for w in text.split() if len(w) > 2]
    # Simple normalized bag-of-words vector representation
    freqs = {}
    for w in words:
        freqs[hash(w) % 128] = freqs.get(hash(w) % 128, 0) + 1
    vec = [freqs.get(i, 0) for i in range(128)]
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = (np.array(vec) / norm).tolist()
    return vec

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes cosine similarity between two vector lists.
    """
    if not vec1 or not vec2:
        return 0.0
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    if len(v1) != len(v2):
        # Handle dimension mismatch if needed
        min_dim = min(len(v1), len(v2))
        v1 = v1[:min_dim]
        v2 = v2[:min_dim]
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))
