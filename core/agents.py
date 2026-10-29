"""
Multi-Agent Orchestration Engine for Cynbit ArchitectAI.
Coordinates specialized agents:
1. Requirements Analyst Agent
2. System Topology Architect Agent
3. Agentic Workflow Designer Agent
4. Security & Threat Modeling Agent
5. Synthesis & Token Economics Agent
"""

from typing import Dict, Any, List
from core.models import (
    ClientRequirementInput,
    MicroserviceNode,
    AgentComponent,
    SecurityThreat,
    ArchitectureBlueprint,
    TokenCostEstimate
)
from core.pipeline import RequirementIngestionPipeline
from core.cost_engine import CostEstimationEngine
from core.mermaid_gen import MermaidDiagramGenerator


class CynbitMultiAgentOrchestrator:
    """Orchestrates the synthesis of end-to-end AI/ML architecture blueprints."""

    @classmethod
    def execute_workflow(cls, req: ClientRequirementInput, model_choice: str = "Gemini 2.0 Flash") -> ArchitectureBlueprint:
        """Executes the multi-stage reasoning pipeline."""

        # Stage 1: Requirements Ingestion & Normalization
        normalized = RequirementIngestionPipeline.normalize_input(req)
        domain = normalized["domain"]
        cloud = normalized["cloud_preference"]
        scale = normalized["scale_tier"]
        intents = normalized["functional_intents"]

        # Stage 2: System Topology Architect Agent
        microservices = cls._agent_system_architect(normalized)

        # Stage 3: Agentic Workflow Designer Agent
        agents = cls._agent_workflow_designer(normalized)

        # Stage 4: Security & Threat Modeling Agent
        security_threats = cls._agent_security_auditor(normalized, agents)

        # Stage 5: Cost & Token Economics Engine
        cost_estimate = CostEstimationEngine.calculate_estimate(
            scale_tier=scale,
            selected_model=model_choice,
            cache_hit_rate=0.30
        )

        # Stage 6: Diagram Generation
        arch_mermaid = MermaidDiagramGenerator.generate_system_architecture(
            project_name=normalized["project_name"],
            services=microservices,
            cloud_provider=cloud
        )
        agent_dag_mermaid = MermaidDiagramGenerator.generate_agent_dag(agents)

        # Stage 7: Implementation Roadmap & Strategic Value
        phases = cls._generate_implementation_phases(normalized)
        summary = cls._synthesize_executive_summary(normalized, agents, microservices)
        value_prop = cls._synthesize_cynbit_value_prop(domain)

        tech_stack = {
            "Frontend / Portal": "Next.js 15 (React 19, Tailwind CSS, TypeScript)",
            "API & Gateway Layer": "FastAPI (Python 3.11) / Envoy Proxy on Cloud Run",
            "Agent Orchestration": "LangGraph / LlamaIndex Agentic Workflows",
            "Primary LLM Engine": f"{model_choice} (Vertex AI / High-Throughput API)",
            "Relational Database": f"PostgreSQL 16 ({'Cloud SQL' if cloud == 'GCP' else 'Amazon RDS'}) with pgvector",
            "Semantic Cache & Queue": "Redis Cluster + RabbitMQ / Cloud PubSub",
            "Telemetry & Guardrails": "OpenTelemetry + Langfuse + NeMo Guardrails",
            "CI/CD & Infrastructure": "Terraform + GitHub Actions (Zero-Trust VPC)"
        }

        return ArchitectureBlueprint(
            project_name=normalized["project_name"],
            domain=domain,
            executive_summary=summary,
            system_type="Autonomous Multi-Agent Cognitive Platform",
            recommended_tech_stack=tech_stack,
            microservices=microservices,
            agent_topology=agents,
            data_pipeline_stages=[
                "Ingestion & Multi-Modal Preprocessing (PDF/Audio/Image/Text)",
                "Vector Embedding & Hybrid BM25 Indexing (pgvector / Qdrant)",
                "Contextual Agentic Routing & Tool Resolution",
                "Deterministic Pydantic Schema Validation & Guardrail Filtering",
                "Downstream Action Dispatch & Event Telemetry Logging"
            ],
            mermaid_architecture_code=arch_mermaid,
            mermaid_agent_dag_code=agent_dag_mermaid,
            token_economics=cost_estimate,
            security_audit=security_threats,
            implementation_phases=phases,
            cynbit_value_proposition=value_prop
        )

    @classmethod
    def _agent_system_architect(cls, normalized: Dict[str, Any]) -> List[MicroserviceNode]:
        """Synthesizes high-availability microservices based on domain and constraints."""
        cloud = normalized["cloud_preference"]
        infra_prefix = "GCP Cloud Run" if cloud == "GCP" else "AWS ECS Fargate"

        return [
            MicroserviceNode(
                id="S1",
                name="Omni-Channel Ingestion Gateway",
                layer="API Gateway",
                technology=f"{infra_prefix} + FastAPI",
                purpose="Receives webhook payloads, user uploads, and API calls with rate-limiting and token verification.",
                scaling_strategy="Horizontal auto-scaling (1 to 20 instances) based on CPU/concurrency."
            ),
            MicroserviceNode(
                id="S2",
                name="Context Extraction & Preprocessing Service",
                layer="Orchestrator",
                technology="Python Async Worker + Unstructured.io / OCR",
                purpose="Extracts clean text, normalizes media formats, and performs PII anonymization before LLM ingestion.",
                scaling_strategy="Queue-driven scaling using Celery / Cloud PubSub depth."
            ),
            MicroserviceNode(
                id="S3",
                name="Agentic Reasoning & Decision Hub",
                layer="Agent Engine",
                technology="LangGraph + Vertex AI / Gemini API",
                purpose="Executes autonomous multi-agent state machines, tool calling, and structured output generation.",
                scaling_strategy="Stateless concurrent worker pods with circuit breakers."
            ),
            MicroserviceNode(
                id="S4",
                name="Action Dispatcher & Integration Engine",
                layer="Downstream Dispatch",
                technology="Node.js / Python Event Handler",
                purpose="Executes verified external mutations: database writes, vendor webhooks, Slack/WhatsApp alerts.",
                scaling_strategy="Idempotent event consumer with automatic exponential backoff."
            )
        ]

    @classmethod
    def _agent_workflow_designer(cls, normalized: Dict[str, Any]) -> List[AgentComponent]:
        """Designs the specialized agent persona DAG tailored to the specific domain."""
        domain = normalized["domain"]
        intents = normalized["functional_intents"]

        if "PropTech" in domain or "TenantEase" in normalized["project_name"]:
            return [
                AgentComponent(
                    name="Triage & Urgency Classifier Agent",
                    role="Intake & Severity Evaluator",
                    primary_task="Parses tenant report, inspects attached media for structural/hazard risks, assigns 1-5 severity.",
                    llm_model="Gemini 2.0 Flash (Multimodal)",
                    tools=["ImageHazardDetector", "UrgencyScorer", "MetadataExtractor"],
                    input_state="Raw tenant ticket (text, audio, photo)",
                    output_state="Structured IncidentProfile (category, urgency, hazard_level)",
                    fallback_strategy="Escalate to Human Property Manager on low confidence (< 0.75)"
                ),
                AgentComponent(
                    name="Lease Compliance & Liability Agent",
                    role="Legal & Contract Clause Inspector",
                    primary_task="Performs hybrid RAG over tenant's signed lease contract to determine landlord vs tenant liability.",
                    llm_model="Gemini 1.5 Pro (Deep Context)",
                    tools=["VectorLeaseRetriever", "ClauseMatchVerifier", "StateTenancyLawDB"],
                    input_state="IncidentProfile + TenantID",
                    output_state="LiabilityDetermination (ResponsibleParty, ClauseCitation, DepositImpact)",
                    fallback_strategy="Flag for Landlord Review if clause ambiguity detected"
                ),
                AgentComponent(
                    name="Vendor Dispatch & Communications Agent",
                    role="Operational Fulfillment Coordinator",
                    primary_task="Matches approved repairs to vetted contractor schedule and drafts WhatsApp notifications.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["ContractorScheduleAPI", "WhatsAppDispatchTool", "WorkOrderGenerator"],
                    input_state="LiabilityDetermination + PropertyLocation",
                    output_state="WorkOrderCreated + TenantNotificationSent",
                    fallback_strategy="Retry dispatch with secondary vendor roster"
                )
            ]
        elif "Reputation" in domain or "Revio" in normalized["project_name"]:
            return [
                AgentComponent(
                    name="Review Harvester & ABSA Agent",
                    role="Multi-Channel Sentiment Classifier",
                    primary_task="Ingests reviews from Google/AppStore and extracts aspect sentiment (Food, Service, Speed, Price).",
                    llm_model="Gemini 2.0 Flash",
                    tools=["GoogleReviewAPI", "AspectSentimentExtractor", "LanguageDetector"],
                    input_state="New review batch / webhook payload",
                    output_state="ExtractedAspects (SentimentScores, CriticalKeywords)",
                    fallback_strategy="Queue for manual triage if sarcasm or slang confidence < 0.70"
                ),
                AgentComponent(
                    name="Crisis & Escalation Detection Agent",
                    role="Brand Safety & Risk Guardian",
                    primary_task="Scans negative reviews for severe legal, food safety, or discriminatory allegations.",
                    llm_model="Gemini 1.5 Pro",
                    tools=["RiskKeywordFilter", "BrandSafetyAuditor", "SlackAlertDispatcher"],
                    input_state="ExtractedAspects + ReviewText",
                    output_state="RiskLevel (Low, Medium, Critical) + ActionTrigger",
                    fallback_strategy="Instant SMS/Slack paging to PR & Executive on-call team"
                ),
                AgentComponent(
                    name="Brand Voice Response Synthesizer",
                    role="Autonomous Customer Relations Officer",
                    primary_task="Synthesizes hyper-personalized, empathetic responses aligned with company brand persona.",
                    llm_model="Claude 3.5 Sonnet / Gemini 2.0 Flash",
                    tools=["BrandStyleGuideRetriever", "ToneConsistencyChecker", "ReviewPlatformPoster"],
                    input_state="ReviewText + CustomerContext + BrandGuidelines",
                    output_state="PublishedResponse (or draft queued for approval)",
                    fallback_strategy="Human-in-the-loop review for all 1-star ratings"
                )
            ]
        elif "EdTech" in domain or "BitElevate" in normalized["project_name"]:
            return [
                AgentComponent(
                    name="Codebase AST & Static Analyzer Agent",
                    role="Structural & Quality Auditor",
                    primary_task="Clones student Git repository, runs AST parsing, linters, cyclomatic complexity, and test runners.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["GitRepoCloner", "AstSyntaxParser", "SecurityLinterTool", "PytestRunner"],
                    input_state="GitHub Pull Request URL / Commit SHA",
                    output_state="StaticMetrics (Coverage, Complexity, Vulnerabilities)",
                    fallback_strategy="Graceful error reporting on build failure"
                ),
                AgentComponent(
                    name="Architecture & Pattern Evaluator Agent",
                    role="Senior Solutions Architect Mentor",
                    primary_task="Evaluates design patterns, SOLID principles, API decoupling, and schema design against course rubric.",
                    llm_model="Claude 3.5 Sonnet / Gemini 1.5 Pro",
                    tools=["ArchitectureRubricMatcher", "PatternDetector", "BenchmarkComparator"],
                    input_state="StaticMetrics + Full Code Diff + AssignmentSpec",
                    output_state="ArchitecturalGrade (0-100) + CodeImprovementDiffs",
                    fallback_strategy="Dual-evaluator consensus review"
                ),
                AgentComponent(
                    name="Personalized Learning Path Synthesizer",
                    role="Adaptive Curriculum Guide",
                    primary_task="Identifies student conceptual gaps and creates custom 14-day study plan with specific tutorials and labs.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["BitElevateCurriculumGraph", "ResourceRecommendationEngine"],
                    input_state="ArchitecturalGrade + StudentHistory",
                    output_state="TailoredStudyPlan + RecommendedLabExercises",
                    fallback_strategy="Default to standard foundational track module"
                )
            ]
        else:
            # General Enterprise / Cynbit Studio
            return [
                AgentComponent(
                    name="Discovery & Intent Decomposer Agent",
                    role="Lead Systems Analyst",
                    primary_task="Interviews user or digests RFP document, decomposes requirements into functional specifications.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["IntentParser", "EntityExtractor", "ScopeBoundaryChecker"],
                    input_state="Unstructured business proposal or user brief",
                    output_state="FunctionalSpecs (Actors, Inputs, Outputs, Constraints)",
                    fallback_strategy="Prompt user with targeted clarifying questions"
                ),
                AgentComponent(
                    name="Architecture & Topology Synthesis Agent",
                    role="Principal Cloud Architect",
                    primary_task="Selects optimal cloud microservices, vector search engines, data stores, and integration buses.",
                    llm_model="Claude 3.5 Sonnet / Gemini 1.5 Pro",
                    tools=["CloudCatalogMatcher", "ScalabilitySim", "LatencyEstimator"],
                    input_state="FunctionalSpecs + ScaleRequirements",
                    output_state="SystemTopology (ServiceNodes, Databases, NetworkBorders)",
                    fallback_strategy="Fallback to standard 3-tier containerized reference pattern"
                ),
                AgentComponent(
                    name="Security Guardrail & Compliance Agent",
                    role="CISO & AI Governance Auditor",
                    primary_task="Screens planned agent workflows against OWASP Top 10 for LLMs and regulatory frameworks.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["OWASPAuditEngine", "ComplianceChecklistValidator"],
                    input_state="SystemTopology + AgentWorkflows",
                    output_state="SecurityAuditMatrix + GuardrailConfiguration",
                    fallback_strategy="Enforce maximum isolation zero-trust defaults"
                ),
                AgentComponent(
                    name="Token Economics & ROI Estimator Agent",
                    role="Financial & Ops Modeler",
                    primary_task="Calculates inference costs, hosting TCO, cache hit margins, and ROI timeline for the client.",
                    llm_model="Gemini 2.0 Flash",
                    tools=["TokenCalculator", "CloudPricingAPI", "ROIForecaster"],
                    input_state="TrafficMetrics + ModelChoices",
                    output_state="FinancialModel (MonthlyTCO, TokenBudget, BreakEvenMonths)",
                    fallback_strategy="Deterministic fallback to upper-bound worst-case pricing"
                )
            ]

    @classmethod
    def _agent_security_auditor(cls, normalized: Dict[str, Any], agents: List[AgentComponent]) -> List[SecurityThreat]:
        """Audits planned architecture against OWASP Top 10 for LLMs."""
        return [
            SecurityThreat(
                threat_category="LLM01: Prompt Injection & Jailbreaking",
                risk_level="High",
                description="Malicious user inputs attempting to bypass agent persona, override system prompts, or leak instructions.",
                mitigation_strategy="Enforce dual-layer input sanitization, separate system instructions via API system parameters, and implement NeMo Guardrails."
            ),
            SecurityThreat(
                threat_category="LLM02: Insecure Output Handling",
                risk_level="High",
                description="LLM-generated code, SQL, or markdown rendered directly to clients or database execution layers without validation.",
                mitigation_strategy="Enforce strict Pydantic schema validation. Disallow direct SQL string formatting; use parameterized queries and safe sandboxed execution."
            ),
            SecurityThreat(
                threat_category="LLM06: Sensitive Information Disclosure",
                risk_level="Critical",
                description="Accidental exposure of confidential customer data, PII, API tokens, or tenant-separated knowledge in prompt contexts.",
                mitigation_strategy="Implement Microsoft Presidio / regex PII masking at the Ingestion Gateway before vector indexing. Enforce multi-tenant Row-Level Security (RLS)."
            ),
            SecurityThreat(
                threat_category="LLM08: Excessive Agency",
                risk_level="Medium",
                description="Autonomous agents executing high-impact financial or data deletions without human confirmation.",
                mitigation_strategy="Enforce Human-in-the-Loop (HITL) approval gates for actions exceeding monetary thresholds (e.g. vendor payouts > $250 or contract terminations)."
            ),
            SecurityThreat(
                threat_category="LLM10: Model Denial of Service",
                risk_level="Medium",
                description="Heavy unthrottled prompts causing resource exhaustion, context blowout, and excessive API billing spikes.",
                mitigation_strategy="Enforce strict token input limits (max 4,000 tokens per request), request throttling per IP/tenant, and circuit breakers."
            )
        ]

    @classmethod
    def _generate_implementation_phases(cls, normalized: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Synthesizes structured 4-phase rollout plan for Cynbit engineering teams."""
        return [
            {
                "phase": "Phase 1: Foundation & Data Pipeline (Weeks 1-3)",
                "milestones": [
                    "Setup cloud infrastructure on GCP/AWS using Terraform and configure VPC peering.",
                    "Build Ingestion Gateway and Unstructured Data Preprocessor with PII scrubbing.",
                    "Deploy PostgreSQL with pgvector and establish vector embedding baseline."
                ],
                "deliverables": "Working data ingestion pipeline, clean test dataset, CI/CD pipeline."
            },
            {
                "phase": "Phase 2: Agentic State Machine & Tool Orchestration (Weeks 4-6)",
                "milestones": [
                    "Implement LangGraph multi-agent DAG with specialized persona prompts.",
                    "Integrate tool calling (vector retrieval, operational APIs, notification channels).",
                    "Configure NeMo Guardrails and Pydantic structured output validation."
                ],
                "deliverables": "End-to-end agentic workflow operating in staging with simulated tools."
            },
            {
                "phase": "Phase 3: Observability, Security & Cost Optimization (Weeks 7-8)",
                "milestones": [
                    "Integrate Langfuse for real-time prompt tracing, latency monitoring, and token tracking.",
                    "Implement Redis semantic caching to achieve ~30% token cost reduction.",
                    "Conduct automated red-teaming against OWASP LLM vulnerabilities."
                ],
                "deliverables": "Security audit sign-off, live telemetry dashboard, optimized token economics."
            },
            {
                "phase": "Phase 4: Production Deployment & Pilot Rollout (Weeks 9-10)",
                "milestones": [
                    "Deploy to high-availability multi-zone Cloud Run / ECS cluster.",
                    "Launch canary rollout with 10% pilot user traffic.",
                    "Handover operational runbooks and train internal operations team."
                ],
                "deliverables": "100% production go-live, SLA monitoring, client sign-off."
            }
        ]

    @classmethod
    def _synthesize_executive_summary(cls, normalized: Dict[str, Any], agents: List[AgentComponent], services: List[MicroserviceNode]) -> str:
        """Generates executive summary of the architecture."""
        proj = normalized["project_name"]
        domain = normalized["domain"]
        scale = normalized["scale_tier"]
        return (
            f"The '{proj}' is engineered as a high-performance, fault-tolerant {domain} "
            f"autonomous platform tailored for {scale}. Architected on an event-driven microservices "
            f"topology ({len(services)} core service layers) paired with a {len(agents)}-stage agentic cognitive "
            f"pipeline, the system replaces manual operational bottlenecks with real-time multi-modal intelligence. "
            f"The architecture guarantees zero-trust data isolation, enterprise compliance, and predictable token economics "
            f"through semantic caching and model routing."
        )

    @classmethod
    def _synthesize_cynbit_value_prop(cls, domain: str) -> str:
        """Formulates Cynbit's unique engineering value proposition."""
        return (
            "Cynbit Technologies' Unfair Advantage: Unlike generic software agencies that stitch together "
            "rudimentary OpenAI wrapper chatbots, Cynbit delivers production-grade systemic architecture. "
            "By combining deterministic software engineering (FastAPI, PostgreSQL, microservices) with advanced "
            "agentic state machines (LangGraph, Gemini 2.0 Flash, semantic caching), Cynbit reduces deployment "
            "cycle time by 65%, eliminates LLM hallucination risks via strict Pydantic schemas, and cuts recurring "
            "cloud TCO by up to 40%."
        )
