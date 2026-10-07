import os
import time
from dotenv import load_dotenv

# Load .env variables
load_dotenv("/home/rida/litlens/.env")

from app.config import settings
from app.services.ai_provider import AIProvider

def test_nvidia_api():
    print("=" * 60)
    print("      NVIDIA NIM LLM API CONNECTION TEST")
    print("=" * 60)

    ai = AIProvider()

    provider = settings.AI_PROVIDER
    nvidia_key_present = bool(settings.NVIDIA_API_KEY and len(settings.NVIDIA_API_KEY) > 10)
    model_name = settings.NVIDIA_MODEL

    print(f"  AI Provider Configured: '{provider}'")
    print(f"  NVIDIA API Key Present: {nvidia_key_present} (Key length: {len(settings.NVIDIA_API_KEY) if settings.NVIDIA_API_KEY else 0})")
    print(f"  Target NVIDIA Model: '{model_name}'")

    if not nvidia_key_present:
        print("\n  [NOTICE] NVIDIA_API_KEY is missing or empty in .env.")
        print("  System will gracefully fallback to local NLP & local sentence embeddings.")
        print("  To enable NVIDIA NIM API, add NVIDIA_API_KEY=nvapi-... to /home/rida/litlens/.env")
        return

    print("\n  Sending request to NVIDIA NIM API (https://integrate.api.nvidia.com/v1)...")
    start_time = time.time()
    
    test_query = "I want a dark mystery under 300 pages with a huge twist and almost no romance"
    result = ai.extract_preferences(test_query)
    elapsed_ms = int((time.time() - start_time) * 1000)

    print(f"  Response Latency: {elapsed_ms} ms")
    print(f"  Extracted Preferences: {result}")
    
    if result and result.get("genre") in ["Mystery", "Any"]:
        print("\n  -> SUCCESS: NVIDIA NIM API Connection verified & working!")
    else:
        print("\n  -> WARNING: API request failed or returned fallback.")

if __name__ == "__main__":
    test_nvidia_api()
