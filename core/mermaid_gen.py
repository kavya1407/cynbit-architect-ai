"""
Mermaid.js Diagram Synthesizer.
Generates robust, syntax-compliant flowcharts for microservices architectures
and multi-agent DAG topologies. Strictly complies with Mermaid rendering rules.
"""

from typing import List
from core.models import MicroserviceNode, AgentComponent


class MermaidDiagramGenerator:
    """Generates valid Mermaid.js diagrams with quoted labels and safe symbols."""

    @classmethod
    def generate_system_architecture(cls, project_name: str, services: List[MicroserviceNode], cloud_provider: str = "GCP") -> str:
        """Generates a complete microservices topology flowchart."""
        lines = [
            "flowchart TD",
            "    %% Cynbit Scalable Architecture Topology",
            "    subgraph ClientLayer[\"Client & Access Layer\"]",
            "        Web[\"Web Application (Next.js / React)\"]",
            "        Mobile[\"Mobile App (Flutter / React Native)\"]",
            "    end",
            "",
            "    subgraph GatewayLayer[\"Edge & Security Gateway\"]",
            "        CDN[\"Cloud CDN & WAF Firewall\"]",
            "        APIGW[\"API Gateway / Reverse Proxy (Envoy / Cloud Run)\"]",
            "    end",
            "",
            "    subgraph CoreServices[\"Core Application & Agent Engine\"]"
        ]

        for s in services:
            clean_name = s.name.replace('"', "'")
            clean_tech = s.technology.replace('"', "'")
            lines.append(f"        {s.id}[\"{clean_name} ({clean_tech})\"]")

        lines.extend([
            "    end",
            "",
            "    subgraph DataPersistence[\"Data & Knowledge Layer\"]",
            f"        DB[(\"Primary DB ({'Cloud SQL Postgres' if cloud_provider == 'GCP' else 'RDS Aurora Postgres'})\")]",
            "        VectorDB[(\"Vector Store (Qdrant / pgvector)\")]",
            "        Cache[(\"Semantic Cache (Redis Cluster)\")]",
            "    end",
            "",
            "    subgraph Observability[\"Telemetry & LLM Governance\"]",
            "        Tracer[\"OpenTelemetry / Langfuse Tracing\"]",
            "        AuditLogs[\"Audit Logger & Policy Guardrails\"]",
            "    end",
            "",
            "    %% Connections",
            "    Web --> CDN",
            "    Mobile --> CDN",
            "    CDN --> APIGW",
            "    APIGW --> S1",
            "    S1 --> S2",
            "    S2 --> S3",
            "    S3 --> S4",
            "    S2 --> Cache",
            "    S3 --> VectorDB",
            "    S4 --> DB",
            "    CoreServices -.-> Tracer",
            "    CoreServices -.-> AuditLogs"
        ])

        return "\n".join(lines)

    @classmethod
    def generate_agent_dag(cls, agents: List[AgentComponent]) -> str:
        """Generates a directed acyclic graph (DAG) of the autonomous agent pipeline."""
        lines = [
            "flowchart LR",
            "    %% Autonomous Agent Orchestration Pipeline",
            "    InputTrigger([\"User Request / Event Hook\"])"
        ]

        prev_id = "InputTrigger"
        for i, agent in enumerate(agents):
            agent_id = f"Agent_{i+1}"
            clean_name = agent.name.replace('"', "'")
            clean_role = agent.role.replace('"', "'")
            clean_model = agent.llm_model.replace('"', "'")
            lines.append(f"    {agent_id}[\"{clean_name}\\nRole: {clean_role}\\nModel: {clean_model}\"]")
            lines.append(f"    {prev_id} --> {agent_id}")
            prev_id = agent_id

        lines.extend([
            f"    {prev_id} --> OutputResponse([\"Synthesized Action / Response\"])",
            "    classDef agentStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;",
            "    classDef triggerStyle fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;"
        ])

        for i in range(len(agents)):
            lines.append(f"    class Agent_{i+1} agentStyle;")
        lines.append("    class InputTrigger,OutputResponse triggerStyle;")

        return "\n".join(lines)
