# LitLens: AI-Driven Natural Language Book Discovery & Recommendation Platform

LitLens is an intelligent, AI-driven book discovery platform that allows readers to express their reading intent in ordinary natural language. The system converts raw natural language into structured reading preferences, performs semantic vector and attribute-based hybrid retrieval against a verified book dataset, transparently ranks candidates, generates spoiler-free explanations, supports single-dimension "Change One Thing" conversational refinement, provides preference-aware side-by-side book comparisons, tracks reading history, generates progressive reading paths, and provides verified access links ("Where to Get It").

---

## 🤖 AI Architecture & API Integration

The repository links to AI models through a **hybrid multi-provider abstraction layer** ([`backend/app/services/ai_provider.py`](backend/app/services/ai_provider.py)):

### 1. NVIDIA NIM LLM Integration (Low Latency)
LitLens integrates natively with [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) using ultra-fast LLM endpoints:
- **Default Model**: `meta/llama-3.1-8b-instruct` (Latency: ~150-200ms)
- **Supported Models**: `mistralai/mistral-7b-instruct-v0.3`, `meta/llama-3.3-70b-instruct`

### 2. Local Sentence-Transformers Embedding Model
Semantic vector search is powered locally by PyTorch and HuggingFace `sentence-transformers` (`all-MiniLM-L6-v2`), running on CPU/GPU without external API dependency.

### 3. Setting Up Your AI API Keys
For security best practices, secret API keys are kept in your local `.env` file (not committed to GitHub). To connect your free NVIDIA NIM API key:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your free NVIDIA API key from [build.nvidia.com](https://build.nvidia.com):
   ```env
   AI_PROVIDER=nvidia
   NVIDIA_API_KEY=nvapi-your_key_here
   NVIDIA_MODEL=meta/llama-3.1-8b-instruct
   ```

---

## Technical Stack

- **Frontend**: Next.js 14+ (App Router), TypeScript, TailwindCSS, Lucide Icons
- **Backend**: Python 3.11, FastAPI, Pydantic, Pytest, Uvicorn
- **AI & NLP**: NVIDIA NIM API, Sentence-Transformers (`all-MiniLM-L6-v2`), NLU Preference Extractor, Spoiler-Free Explanation Generator
- **Database**: PostgreSQL / Supabase Schema (Relational SQLite Driver for zero-config offline execution)

---

## Core Features

1. **Natural-Language Search (P0)**: Enter prompts like *"I want a short dark mystery under 300 pages with a huge plot twist and almost no romance"*.
2. **AI Book Matching & Transparent Ranking (P0)**: Computes a multi-signal match score combining semantic similarity, constraint satisfaction, and Book DNA compatibility.
3. **Structured Book DNA (P0)**: Detailed profiles storing Mood, Pacing, Romance Level, Complexity, Emotional Intensity, Setting, and Themes.
4. **"Where to Get It" Verified Access Links (NEW)**: Direct access buttons for verified providers (Open Library read/borrow, Google Books buy, Amazon buy).
5. **"Change One Thing" Conversational Refinement (P0)**: Modify specific preference dimensions (e.g. *"Make it darker"*, *"Shorter"*, *"Less romance"*) while preserving active context.
6. **Preference-Aware Side-by-Side Comparison (P0)**: Evaluates selected candidate books against active reading intent with an AI verdict.
7. **Spoiler-Free Explanations (P0)**: Controlled prompt rules preventing story reveals while highlighting why a book matches.
8. **Personal Reading History (P1)**: Track saved, read, reading, and rejected books. Disliked books receive recommendation penalties.
9. **Progressive Reading Paths (P1)**: Sequence books across Entry, Intermediate, and Mastery tiers ordered by complexity and length.
10. **Evaluation Engine & Comparative Experiment**: Precision@K metrics and comparative benchmark between conventional metadata search vs. natural language search.

---

## System Architecture

```
                 USER
                   │
                   ▼
          NEXT.JS + TYPESCRIPT (Port 3000)
                   │
                   ▼
             PYTHON / FASTAPI (Port 8000)
                   │
   ┌───────────────┼───────────────┐
   ▼               ▼               ▼
NVIDIA NIM /   Sentence-        Hybrid Scoring
Gemini LLM     Transformers     Ranker Engine
(build.nvidia) (MiniLM-L6-v2)   (Score = 0.35 Sim + 0.25 Const + 0.40 DNA)
   │               │               │
   └───────────────┼───────────────┘
                   ▼
             Database Schema
          (Books, Attributes, DNA, Availability)
```

---

## Quick Start & Setup

### 1. Backend Setup
```bash
source .venv/bin/activate
PYTHONPATH=backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm run dev -- -p 3000
```

### 3. Running Tests & Audits
```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests/
PYTHONPATH=backend .venv/bin/python backend/tests/verify_all_requirements.py
PYTHONPATH=backend .venv/bin/python backend/tests/deep_audit_backtest.py
```
