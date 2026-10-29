"""
Pre-configured real-world case study templates for Cynbit Technologies.
Provides instant, production-accurate demos across Cynbit's key product and service domains.
"""

from typing import Dict, Any


SAMPLE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "TenantEase AI (PropTech Maintenance & Lease Agent)": {
        "project_name": "TenantEase Autonomous Maintenance & Lease Triage Engine",
        "industry_domain": "PropTech / Real Estate",
        "problem_statement": """
TenantEase needs an intelligent autonomous triage system for residential property management.
Tenants frequently report maintenance issues (plumbing leaks, electrical faults, HVAC failures)
via text, audio notes, and uploaded photos. Currently, property managers spend hours manually reviewing
tickets, assessing urgency, contacting vendors, and parsing lease agreements to verify landlord vs tenant liability.

We need an AI agent system that:
1. Ingests multimodal tenant reports (photos, voice notes, and text).
2. Classifies maintenance category, severity score (1-5), and emergency risk.
3. Queries vector-indexed lease agreements to determine liability clause (Tenant vs Landlord).
4. Automatically drafts vendor work orders and sends WhatsApp updates to tenants and property managers.
5. Integrates with the TenantEase property management PostgreSQL database.
""",
        "target_users": "Tenants, Property Managers, and Maintenance Contractors",
        "expected_scale": "Medium (10k - 100k MAU)",
        "cloud_preference": "GCP",
        "compliance_needs": ["GDPR", "Local Tenancy Law Compliance", "Data Isolation"],
        "budget_tier": "Growth / Enterprise"
    },

    "Revio AI (Customer Sentiment & Review Engine)": {
        "project_name": "Revio Autonomous Sentiment-to-Action & Review Orchestrator",
        "industry_domain": "Reputation & Customer Sentiment",
        "problem_statement": """
Revio empowers multi-location brands and SaaS companies to manage online reputation.
Currently, client brands receive hundreds of Google Reviews, Trustpilot feedback, and App Store ratings daily.
Negative reviews linger for days without human response, causing customer churn and hurting SEO rankings.

We want an autonomous AI system that:
1. Monitors reviews across Google, Trustpilot, and App Store in real-time.
2. Performs Aspect-Based Sentiment Analysis (ABSA) detecting product quality, staff behavior, pricing, and turnaround time.
3. Detects urgent escalation signals (legal threats, food poisoning, major safety or billing bugs) and alerts managers via Slack/Webhooks.
4. Synthesizes brand-aligned, empathetic responses tailored to brand voice guidelines and posts drafts for approval or auto-publishes based on confidence threshold.
5. Generates weekly executive digest summarizing sentiment trends and product improvement recommendations.
""",
        "target_users": "Brand Marketing Directors, Support Managers, and Franchise Owners",
        "expected_scale": "High (100k - 1M MAU)",
        "cloud_preference": "AWS",
        "compliance_needs": ["SOC2-ready", "Brand Safety Guardrails"],
        "budget_tier": "Enterprise"
    },

    "BitElevate AI (Architectural Code & Project Evaluator)": {
        "project_name": "BitElevate Autonomous Code & System Architecture Evaluator",
        "industry_domain": "EdTech & Developer Upskilling",
        "problem_statement": """
BitElevate transitions students and junior developers into production software architects.
Mentors are overwhelmed grading hundreds of student repositories, checking clean code practices,
system architecture choices, test coverage, and documentation quality.

We need an AI-driven Engineering Lab Mentor that:
1. Ingests student GitHub repositories via webhook on Pull Request.
2. Analyzes code structure, architectural layering (Separation of Concerns, DRY, SOLID principles).
3. Identifies anti-patterns, security vulnerabilities (SQL injection, hardcoded secrets), and missing tests.
4. Generates an interactive architectural rubric score (0-100) and actionable code suggestions.
5. Creates a personalized 2-week learning path recommending specific documentation, coding exercises, and system design reading.
""",
        "target_users": "BitElevate Students, Interns, and Senior Engineering Mentors",
        "expected_scale": "Small (< 10k MAU)",
        "cloud_preference": "GCP",
        "compliance_needs": ["Data Privacy", "FERPA-aligned"],
        "budget_tier": "Startup / Growth"
    },

    "Cynbit Studio Omnichannel Discovery & Intake Agent": {
        "project_name": "Cynbit Studio Autonomous Discovery & Solution Architect",
        "industry_domain": "Enterprise Document & Operations",
        "problem_statement": """
Cynbit receives inbound enterprise client inquiries for custom software, mobile apps, and autonomous AI systems.
Clients provide vague or complex requirement briefs. Senior architects spend 10-15 hours per prospect
conducting discovery interviews, scoping technical feasibility, choosing cloud stacks, drawing architecture diagrams,
and estimating token/cloud budgets.

We require an autonomous AI Solutions Architect that:
1. Conducts an interactive technical discovery interview with prospective clients.
2. Extracts functional specifications, non-functional constraints (latency, concurrency, compliance), and scale metrics.
3. Automatically maps requirements to optimal microservices, vector databases, and multi-agent topologies.
4. Generates Mermaid.js architectural blueprints and calculates token economics / monthly cloud TCO.
5. Synthesizes an executive-ready proposal document and downloadable architecture specification in under 60 seconds.
""",
        "target_users": "Prospective Enterprise Clients, Cynbit Account Executives, and Solutions Architects",
        "expected_scale": "Medium (10k - 100k MAU)",
        "cloud_preference": "GCP",
        "compliance_needs": ["Enterprise Confidentiality", "SOC2-ready", "GDPR"],
        "budget_tier": "Growth / Enterprise"
    }
}
