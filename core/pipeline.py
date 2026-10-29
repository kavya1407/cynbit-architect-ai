"""
Input normalization and data extraction pipeline for unstructured client briefs.
Parses messy client requests, extracts key functional requirements, non-functional
constraints, scale parameters, and domain semantics.
"""

import re
from typing import Dict, Any, List
from core.models import ClientRequirementInput


class RequirementIngestionPipeline:
    """Extracts structured entities, functional requirements, and constraints from free-text briefs."""

    DOMAIN_KEYWORDS = {
        "PropTech / Real Estate": ["tenant", "lease", "rent", "property", "landlord", "maintenance", "repair", "apartment", "building", "tenantease"],
        "Reputation & Customer Sentiment": ["review", "feedback", "rating", "sentiment", "customer support", "complaint", "reputation", "revio", "churn"],
        "EdTech & Developer Upskilling": ["code", "student", "grading", "learn", "curriculum", "bitelevate", "review code", "intern", "assignment", "skills"],
        "Healthcare & Telemedicine": ["patient", "doctor", "clinic", "medical", "appointment", "prescription", "health", "diagnosis", "hipaa"],
        "FinTech & Banking": ["payment", "fraud", "loan", "bank", "invoice", "credit", "transaction", "kyc", "accounting", "ledger"],
        "E-Commerce & Retail": ["catalog", "cart", "order", "inventory", "checkout", "shipping", "product", "e-commerce", "recommendation"],
        "Enterprise Document & Operations": ["pdf", "invoice", "contract", "workflow", "document", "extract", "ocr", "procurement", "enterprise"]
    }

    SCALE_MAP = {
        "Small (< 10k MAU)": {"mau": 5000, "infra_mult": 1.0, "llm_volume": 10000},
        "Medium (10k - 100k MAU)": {"mau": 50000, "infra_mult": 2.5, "llm_volume": 100000},
        "High (100k - 1M MAU)": {"mau": 500000, "infra_mult": 6.0, "llm_volume": 1000000},
        "Enterprise (> 1M MAU)": {"mau": 2000000, "infra_mult": 15.0, "llm_volume": 5000000}
    }

    @classmethod
    def detect_domain(cls, text: str, fallback_domain: str = "General Enterprise") -> str:
        """Heuristically detects domain if not specified or refines selected domain."""
        text_lower = text.lower()
        scores = {}
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
            if score > 0:
                scores[domain] = score
        
        if scores:
            best_domain = max(scores, key=scores.get)
            return best_domain
        return fallback_domain

    @classmethod
    def extract_functional_intents(cls, text: str) -> List[str]:
        """Extracts bulleted or implied functional capabilities from text."""
        sentences = [s.strip() for s in re.split(r'[.\n;•-]', text) if len(s.strip()) > 10]
        intents = []
        action_verbs = ["automate", "extract", "generate", "route", "classify", "detect", "summarize", "integrate", "monitor", "alert", "dispatch", "triage", "evaluate"]
        
        for s in sentences:
            if any(verb in s.lower() for verb in action_verbs):
                intents.append(s)
            elif len(intents) < 5 and len(s) > 15:
                intents.append(s)
        
        if not intents:
            intents = [
                "Automated ingestion and parsing of multi-modal user requests",
                "Contextual reasoning and decision routing via specialized LLM agents",
                "Real-time integration with downstream operational databases and external APIs",
                "Continuous feedback monitoring and audit logging for system reliability"
            ]
        return intents[:6]

    @classmethod
    def normalize_input(cls, req: ClientRequirementInput) -> Dict[str, Any]:
        """Normalizes and enriches the client requirement object."""
        combined_text = f"{req.project_name} {req.industry_domain} {req.problem_statement}"
        detected_domain = cls.detect_domain(combined_text, req.industry_domain)
        intents = cls.extract_functional_intents(req.problem_statement)
        scale_data = cls.SCALE_MAP.get(req.expected_scale, cls.SCALE_MAP["Medium (10k - 100k MAU)"])

        return {
            "project_name": req.project_name.strip() or "Cynbit Autonomous Platform",
            "domain": detected_domain,
            "raw_problem": req.problem_statement.strip(),
            "target_users": req.target_users,
            "scale_tier": req.expected_scale,
            "scale_metrics": scale_data,
            "cloud_preference": req.cloud_preference,
            "compliance_needs": req.compliance_needs,
            "budget_tier": req.budget_tier,
            "functional_intents": intents
        }
