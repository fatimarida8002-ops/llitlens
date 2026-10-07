from fastapi import APIRouter
from app.services.evaluation import evaluator

router = APIRouter()

@router.get("/evaluation/experiment")
def run_evaluation_experiment():
    return evaluator.run_conventional_vs_nl_experiment()
