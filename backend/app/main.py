from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, ensure_default_user
from app.ingestion.open_library import seed_books_to_db

from app.api import discover, refine, compare, books, history, reading_path, evaluation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Database Initialization & Seed Data Ingestion
    init_db()
    ensure_default_user()
    seed_books_to_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(discover.router, prefix=settings.API_PREFIX, tags=["Discover"])
app.include_router(refine.router, prefix=settings.API_PREFIX, tags=["Conversational Refinement"])
app.include_router(compare.router, prefix=settings.API_PREFIX, tags=["Comparison"])
app.include_router(books.router, prefix=settings.API_PREFIX, tags=["Books"])
app.include_router(history.router, prefix=settings.API_PREFIX, tags=["Reading History"])
app.include_router(reading_path.router, prefix=settings.API_PREFIX, tags=["Reading Paths"])
app.include_router(evaluation.router, prefix=settings.API_PREFIX, tags=["Evaluation"])

@app.get("/")
def root():
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
