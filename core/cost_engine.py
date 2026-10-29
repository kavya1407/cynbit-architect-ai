"""
Token Economics and Cloud Infrastructure Cost Modeling Engine.
Calculates token budgets, monthly recurring costs (inference + hosting),
and architectural cost-saving recommendations (semantic caching, prompt compression).
"""

from typing import Dict, Any, List
from core.models import TokenCostEstimate


class CostEstimationEngine:
    """Calculates LLM token consumption and cloud operational expenditures."""

    # Pricing per 1 Million Tokens (USD)
    MODEL_PRICING = {
        "Gemini 2.0 Flash": {"input": 0.10, "output": 0.40, "desc": "Ultra-low latency, high throughput, optimal for high-volume agents"},
        "Gemini 1.5 Pro": {"input": 1.25, "output": 5.00, "desc": "Complex multimodal reasoning and large 2M context window"},
        "Claude 3.5 Sonnet": {"input": 3.00, "output": 15.00, "desc": "Superior coding, deep architectural reasoning, and precision"},
        "GPT-4o-mini": {"input": 0.15, "output": 0.60, "desc": "Fast, cost-efficient general reasoning"},
        "Open-Source (Llama 3.3 70B Self-Hosted vLLM)": {"input": 0.40, "output": 0.80, "desc": "Private data isolation on dedicated GPU nodes (A10G/L4)"}
    }

    # Base cloud infrastructure tiers (Compute, Managed DB, Vector DB, Networking)
    INFRA_TIER_COSTS = {
        "Small (< 10k MAU)": 150.0,
        "Medium (10k - 100k MAU)": 550.0,
        "High (100k - 1M MAU)": 1800.0,
        "Enterprise (> 1M MAU)": 4500.0
    }

    @classmethod
    def calculate_estimate(
        cls,
        scale_tier: str,
        selected_model: str = "Gemini 2.0 Flash",
        custom_mau: int = None,
        custom_reqs_per_user: int = 15,
        avg_input_tokens: int = 1200,
        avg_output_tokens: int = 400,
        cache_hit_rate: float = 0.25
    ) -> TokenCostEstimate:
        """Computes monthly inference and infrastructure cost breakdown."""
        
        # Determine MAU
        if custom_mau:
            mau = custom_mau
        elif "Small" in scale_tier:
            mau = 8000
        elif "High" in scale_tier:
            mau = 350000
        elif "Enterprise" in scale_tier:
            mau = 1500000
        else:
            mau = 50000  # Medium default

        total_requests = mau * custom_reqs_per_user
        
        # Factoring semantic cache hits (uncached requests require full LLM call)
        effective_requests = total_requests * (1.0 - cache_hit_rate)
        
        # Token totals in Millions
        total_input_tokens_m = (effective_requests * avg_input_tokens) / 1_000_000.0
        total_output_tokens_m = (effective_requests * avg_output_tokens) / 1_000_000.0

        pricing = cls.MODEL_PRICING.get(selected_model, cls.MODEL_PRICING["Gemini 2.0 Flash"])
        input_rate = pricing["input"]
        output_rate = pricing["output"]

        monthly_llm_cost = (total_input_tokens_m * input_rate) + (total_output_tokens_m * output_rate)
        monthly_infra_cost = cls.INFRA_TIER_COSTS.get(scale_tier, 550.0)
        total_monthly_cost = round(monthly_llm_cost + monthly_infra_cost, 2)

        recommendations = [
            f"Implement Semantic Caching (Redis/Momento) to capture ~{int(cache_hit_rate*100)}% recurring queries, saving approx ${(total_requests * cache_hit_rate * (avg_input_tokens * input_rate + avg_output_tokens * output_rate) / 1_000_000.0):.2f}/mo.",
            "Use Model Tiering / Routing: Route trivial triage requests to lightweight models (Gemini 2.0 Flash) and reserve flagship models (Gemini 1.5 Pro / Claude 3.5 Sonnet) for complex multi-step reasoning.",
            "Enforce strict token truncation and system prompt compression with Pydantic JSON schemas to eliminate redundant conversational tokens.",
            "Utilize prompt caching (supported on Gemini and Anthropic) to discount repetitive system instructions by up to 50-75%."
        ]

        return TokenCostEstimate(
            monthly_active_users=mau,
            requests_per_user_month=custom_reqs_per_user,
            avg_input_tokens_per_req=avg_input_tokens,
            avg_output_tokens_per_req=avg_output_tokens,
            total_monthly_input_tokens_m=round(total_input_tokens_m, 3),
            total_monthly_output_tokens_m=round(total_output_tokens_m, 3),
            selected_model=selected_model,
            model_input_cost_per_m=input_rate,
            model_output_cost_per_m=output_rate,
            monthly_llm_inference_cost_usd=round(monthly_llm_cost, 2),
            monthly_cloud_infra_cost_usd=round(monthly_infra_cost, 2),
            total_estimated_monthly_cost_usd=total_monthly_cost,
            cost_saving_recommendations=recommendations
        )
