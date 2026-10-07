# LitLens: AI-Driven Natural Language Book Discovery & Recommendation Platform

LitLens is an intelligent, AI-driven book discovery platform that allows readers to express their reading intent in ordinary natural language. The system converts raw natural language into structured reading preferences, performs semantic vector and attribute-based hybrid retrieval against a verified book dataset, transparently ranks candidates, generates spoiler-free explanations, supports single-dimension "Change One Thing" conversational refinement, provides preference-aware side-by-side book comparisons, tracks reading history, and generates progressive reading paths.

---

## Technical Stack

- **Frontend**: Next.js 14+ (App Router), TypeScript, TailwindCSS, Lucide Icons
- **Backend**: Python 3.11, FastAPI, Pydantic, Pytest, Uvicorn
- **AI & NLP**: Sentence-Transformers (`all-MiniLM-L6-v2`), NLU Structured Preference Extractor, Spoiler-Free Explanation Generator, AI Provider Abstraction (Ollama / Gemini / Heuristic Fallback)
- **Database**: PostgreSQL / Supabase Schema (Relational SQLite Driver for zero-config offline execution)

---

## Core Features

1. **Natural-Language Search (P0)**: Enter prompts like *"I want a short dark mystery under 300 pages with a huge plot twist and almost no romance"*.
2. **AI Book Matching & Transparent Ranking (P0)**: Computes a multi-signal match score combining semantic similarity, constraint satisfaction, and Book DNA compatibility.
3. **Structured Book DNA (P0)**: Detailed profiles storing Mood, Pacing, Romance Level, Complexity, Emotional Intensity, Setting, and Themes.
4. **"Change One Thing" Conversational Refinement (P0)**: Modify specific preference dimensions (e.g. *"Make it darker"*, *"Shorter"*, *"Less romance"*) while preserving active context.
5. **Preference-Aware Side-by-Side Comparison (P0)**: Evaluates selected candidate books against active reading intent with an AI verdict.
6. **Spoiler-Free Explanations (P0)**: Controlled prompt rules preventing story reveals while highlighting why a book matches.
7. **Personal Reading History (P1)**: Track saved, read, reading, and rejected books. Disliked books receive recommendation penalties.
8. **Progressive Reading Paths (P1)**: Sequence books across Entry, Intermediate, and Mastery tiers ordered by complexity and length.
9. **Evaluation Engine & Comparative Experiment**: Precision@K metrics and comparative benchmark between conventional metadata search vs. natural language search.

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
NLU / AI       Retrieval       Ranker Engine
Provider       Engine          (Score = 0.35 Sim + 0.25 Const + 0.40 DNA)
   │               │               │
   └───────────────┼───────────────┘
                   ▼
             Database Schema
          (Books, Attributes, DNA)
```

---

## Quick Start & Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 20+

### 2. Backend Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH and start FastAPI server
PYTHONPATH=backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
export PATH=/home/rida/litlens/.node/bin:$PATH # or your Node path
npm run dev -- -p 3000
```

### 4. Running Tests & System Audit
```bash
# Run backend pytest suite
PYTHONPATH=backend .venv/bin/pytest backend/tests/test_backend.py

# Run complete requirement evidence audit
PYTHONPATH=backend .venv/bin/python backend/tests/verify_all_requirements.py
```

---

## Final Project Positioning

LitLens positions its core contribution around the **integrated workflow**:
Natural-language intent → Structured preference extraction → Semantic & Book DNA retrieval → Transparent hybrid ranking → Conversational refinement → Preference-aware comparison → Spoiler-free explanation → Persistent user history → Progressive reading paths.
