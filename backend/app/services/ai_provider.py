import json
import re
import requests
from typing import Dict, Any, Optional
from app.config import settings

class AIProvider:
    """
    Clean AI Abstraction Layer supporting NVIDIA NIM, Gemini, Ollama, and Local Heuristic Fallback.
    """
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        self.nvidia_key = settings.NVIDIA_API_KEY
        self.nvidia_model = settings.NVIDIA_MODEL
        self.nvidia_url = settings.NVIDIA_BASE_URL
        self.gemini_key = settings.GEMINI_API_KEY
        self.ollama_url = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL

    def extract_preferences(self, user_query: str) -> Dict[str, Any]:
        """
        Converts natural language reading intent into structured preferences.
        """
        prompt = f"""You are an expert literary curator and AI reading assistant.
Analyze the user's natural language request for a book and extract structured reading preferences into a valid JSON object.

User Request: "{user_query}"

Respond ONLY with a valid JSON object matching this exact structure:
{{
    "genre": "Mystery | Fantasy | Sci-Fi | Romance | Literary | Non-Fiction | Any",
    "subgenre": "string or empty",
    "mood": "Dark | Suspenseful | Comforting | Thought-provoking | Atmospheric | Uplifting | Funny | Mysterious | Any",
    "pacing": "Fast | Medium | Slow | Any",
    "romance_level": "None | Low | Medium | High | Any",
    "complexity": "Easy | Medium | High | Any",
    "max_pages": integer or null (e.g. 300 if user asks for under 300 pages),
    "explicit_constraints": ["list of explicit negative or positive rules"],
    "themes": ["list of key themes mentioned"]
}}
"""
        # 1. Try NVIDIA NIM API if key is present (Low latency fast inference)
        if self.provider in ["auto", "nvidia"] and self.nvidia_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.nvidia_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.nvidia_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 512
                }
                resp = requests.post(f"{self.nvidia_url}/chat/completions", headers=headers, json=payload, timeout=4)
                if resp.status_code == 200:
                    text = resp.json()["choices"][0]["message"]["content"]
                    parsed = self._clean_and_parse_json(text)
                    if parsed:
                        return self._normalize_extracted_prefs(parsed, user_query)
            except Exception:
                pass

        # 2. Try Gemini if API key is present
        if self.provider in ["auto", "gemini"] and self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel(settings.AI_MODEL)
                response = model.generate_content(prompt)
                parsed = self._clean_and_parse_json(response.text)
                if parsed:
                    return self._normalize_extracted_prefs(parsed, user_query)
            except Exception:
                pass

        # 3. Try Ollama if available
        if self.provider in ["auto", "ollama"]:
            try:
                resp = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={"model": self.ollama_model, "prompt": prompt, "stream": False},
                    timeout=5
                )
                if resp.status_code == 200:
                    text = resp.json().get("response", "")
                    parsed = self._clean_and_parse_json(text)
                    if parsed:
                        return self._normalize_extracted_prefs(parsed, user_query)
            except Exception:
                pass
                
        # 4. Graceful Rule-Based Local NLP Fallback Engine
        return self._heuristic_preference_extraction(user_query)

    def generate_spoiler_free_explanation(
        self, book_title: str, author: str, book_description: str, user_intent: str, match_score: float
    ) -> str:
        """
        Generates a spoiler-safe explanation why a book matches the user's intent.
        """
        prompt = f"""Provide a concise, spoiler-free recommendation explanation (2-3 sentences max).
Book: {book_title} by {author}
Description: {book_description}
User Intent: {user_intent}
Match Score: {int(match_score * 100)}%

CRITICAL SAFETY DIRECTIVE:
Do NOT reveal major plot twists, murderer identities, secret reveals, or character deaths.
Explain why the tone, pacing, genre, and reading experience match what the user requested.
"""
        # Try NVIDIA NIM first if present
        if self.provider in ["auto", "nvidia"] and self.nvidia_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.nvidia_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.nvidia_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 256
                }
                resp = requests.post(f"{self.nvidia_url}/chat/completions", headers=headers, json=payload, timeout=4)
                if resp.status_code == 200:
                    text = resp.json()["choices"][0]["message"]["content"]
                    if text:
                        return text.strip()
            except Exception:
                pass

        if self.provider in ["auto", "gemini"] and self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel(settings.AI_MODEL)
                res = model.generate_content(prompt)
                if res.text:
                    return res.text.strip()
            except Exception:
                pass

        # Fallback spoiler-safe synthesis
        return (
            f"'{book_title}' is a strong match ({int(match_score * 100)}% compatibility) for your intent. "
            f"It aligns with your requested style, mood, and genre expectations without revealing any story spoilers."
        )

    def _heuristic_preference_extraction(self, text: str) -> Dict[str, Any]:
        """
        Deterministic NLP extractor guaranteeing valid structured preferences offline.
        """
        t = text.lower()
        
        # Genre detection
        genre = "Any"
        if "mystery" in t or "thriller" in t or "crime" in t or "murder" in t:
            genre = "Mystery"
        elif "fantasy" in t or "magic" in t or "wizard" in t:
            genre = "Fantasy"
        elif "sci-fi" in t or "scifi" in t or "space" in t or "future" in t:
            genre = "Sci-Fi"
        elif "romance" in t or "love story" in t:
            genre = "Romance"
        elif "literary" in t or "contemporary" in t:
            genre = "Literary"

        # Mood detection
        mood = "Any"
        if "dark" in t or "grim" in t:
            mood = "Dark"
        elif "suspense" in t or "tense" in t:
            mood = "Suspenseful"
        elif "comfort" in t or "cozy" in t or "warm" in t:
            mood = "Comforting"
        elif "thought" in t or "mind" in t or "philosophical" in t:
            mood = "Thought-provoking"
        elif "atmosphere" in t or "gothic" in t:
            mood = "Atmospheric"
        elif "uplifting" in t or "happy" in t:
            mood = "Uplifting"
        elif "funny" in t or "humorous" in t:
            mood = "Funny"

        # Page count detection
        max_pages = None
        match_pages = re.search(r'(under|less than|max|below)\s*(\d{3,4})', t)
        if match_pages:
            max_pages = int(match_pages.group(2))
        elif "short" in t:
            max_pages = 320
        elif "long" in t or "epic" in t:
            max_pages = 700

        # Romance level
        romance = "Any"
        if "no romance" in t or "little romance" in t or "almost no romance" in t or "without romance" in t:
            romance = "Low"
        elif "high romance" in t or "lots of romance" in t:
            romance = "High"

        # Pacing
        pacing = "Any"
        if "fast" in t or "quick" in t or "page turner" in t:
            pacing = "Fast"
        elif "slow" in t or "unhurried" in t:
            pacing = "Slow"

        # Complexity
        complexity = "Any"
        if "easy" in t or "simple" in t or "light" in t:
            complexity = "Easy"
        elif "complex" in t or "deep" in t or "challenging" in t:
            complexity = "High"

        return {
            "genre": genre,
            "subgenre": "",
            "mood": mood,
            "pacing": pacing,
            "romance_level": romance,
            "complexity": complexity,
            "max_pages": max_pages,
            "explicit_constraints": [s.strip() for s in text.split(",") if "no " in s.lower() or "not " in s.lower()],
            "themes": [w for w in ["identity", "survival", "magic", "crime", "space", "grief", "family"] if w in t]
        }

    def _normalize_extracted_prefs(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        defaults = self._heuristic_preference_extraction(query)
        for key, val in defaults.items():
            if key not in data or data[key] is None or data[key] == "":
                data[key] = val
        return data

    def _clean_and_parse_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        try:
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None

ai_provider = AIProvider()
