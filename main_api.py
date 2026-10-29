"""
FastAPI REST Service for Cynbit ArchitectAI.
Exposes endpoints for headless synthesis, token cost calculations, and CI/CD integrations.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from core.models import ClientRequirementInput, ArchitectureBlueprint, TokenCostEstimate
from core.agents import CynbitMultiAgentOrchestrator
from core.cost_engine import CostEstimationEngine
from core.templates import SAMPLE_TEMPLATES

app = FastAPI(
    title="Cynbit ArchitectAI API",
    description="Autonomous System Architecture and Multi-Agent Workflow Engine for Cynbit Technologies",
    version="1.0.0"
)


class CostRequest(BaseModel):
    scale_tier: str = "Medium (10k - 100k MAU)"
    selected_model: str = "Gemini 2.0 Flash"
    mau: Optional[int] = 50000
    requests_per_user: Optional[int] = 15
    cache_hit_rate: Optional[float] = 0.30


@app.get("/api/v1/health")
def healthcheck():
    """Service health and readiness check."""
    return {
        "status": "healthy",
        "service": "Cynbit ArchitectAI",
        "version": "1.0.0",
        "company": "Cynbit Technologies Private Limited",
        "engine": "Multi-Agent Synthesis Engine"
    }


@app.get("/api/v1/templates")
def list_templates():
    """Lists pre-configured benchmarks for Cynbit products (TenantEase, Revio, BitElevate, Studio)."""
    return {
        "templates": list(SAMPLE_TEMPLATES.keys()),
        "details": SAMPLE_TEMPLATES
    }


@app.post("/api/v1/synthesize", response_model=ArchitectureBlueprint)
def synthesize_architecture(req: ClientRequirementInput, model_choice: str = "Gemini 2.0 Flash"):
    """
    Synthesizes a full microservices architecture, agentic DAG,
    token cost model, and security audit from client requirements.
    """
    try:
        blueprint = CynbitMultiAgentOrchestrator.execute_workflow(req, model_choice=model_choice)
        return blueprint
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Architecture synthesis failed: {str(e)}")


@app.post("/api/v1/estimate-cost", response_model=TokenCostEstimate)
def estimate_cost(req: CostRequest):
    """Calculates granular token economics and cloud infrastructure costs."""
    try:
        return CostEstimationEngine.calculate_estimate(
            scale_tier=req.scale_tier,
            selected_model=req.selected_model,
            custom_mau=req.mau,
            custom_reqs_per_user=req.requests_per_user,
            cache_hit_rate=req.cache_hit_rate
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cost calculation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
