"""
Unit and Integration Tests for Cynbit ArchitectAI using standard unittest.
Tests schema validation, domain classification, agent orchestration,
cost economics, Mermaid generation, and model schemas.
"""

import unittest
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import ClientRequirementInput, MicroserviceNode, AgentComponent
from core.pipeline import RequirementIngestionPipeline
from core.cost_engine import CostEstimationEngine
from core.mermaid_gen import MermaidDiagramGenerator
from core.agents import CynbitMultiAgentOrchestrator
from core.templates import SAMPLE_TEMPLATES


class TestCynbitArchitectAI(unittest.TestCase):

    def test_domain_detection(self):
        """Verify that domain detection maps keywords accurately."""
        proptech_text = "Tenants have leaky plumbing and need lease agreement checks."
        detected = RequirementIngestionPipeline.detect_domain(proptech_text)
        self.assertIn("PropTech", detected)

        sentiment_text = "We need to analyze Google reviews, sentiment ratings, and customer churn."
        detected_sent = RequirementIngestionPipeline.detect_domain(sentiment_text)
        self.assertIn("Reputation", detected_sent)

        edtech_text = "BitElevate students submit code repositories and need mentor review."
        detected_ed = RequirementIngestionPipeline.detect_domain(edtech_text)
        self.assertIn("EdTech", detected_ed)

    def test_cost_estimation_engine(self):
        """Verify token economics formulas and caching logic."""
        cost = CostEstimationEngine.calculate_estimate(
            scale_tier="Medium (10k - 100k MAU)",
            selected_model="Gemini 2.0 Flash",
            custom_mau=50000,
            custom_reqs_per_user=10,
            cache_hit_rate=0.20
        )
        self.assertEqual(cost.monthly_active_users, 50000)
        self.assertGreater(cost.total_estimated_monthly_cost_usd, 0)
        self.assertEqual(cost.monthly_cloud_infra_cost_usd, 550.0)
        self.assertGreaterEqual(len(cost.cost_saving_recommendations), 3)

    def test_mermaid_syntax_compliance(self):
        """Ensure generated Mermaid diagrams are syntactically safe and contain quoted labels."""
        services = [
            MicroserviceNode(
                id="S1",
                name="API Gateway",
                layer="Gateway",
                technology="FastAPI",
                purpose="Ingestion",
                scaling_strategy="Horizontal"
            )
        ]
        code = MermaidDiagramGenerator.generate_system_architecture("Test Project", services, "GCP")
        self.assertIn("flowchart TD", code)
        self.assertIn('S1["API Gateway (FastAPI)"]', code)

        agents = [
            AgentComponent(
                name="Triage Agent",
                role="Classifier",
                primary_task="Classifies tickets",
                llm_model="Gemini 2.0 Flash",
                tools=["ImageDetector"],
                input_state="Raw Ticket",
                output_state="Incident Profile",
                fallback_strategy="Escalate"
            )
        ]
        dag_code = MermaidDiagramGenerator.generate_agent_dag(agents)
        self.assertIn("flowchart LR", dag_code)
        self.assertIn("Agent_1", dag_code)

    def test_all_cynbit_templates_orchestration(self):
        """Verify orchestrator runs cleanly across all pre-configured Cynbit product templates."""
        for t_name, t_data in SAMPLE_TEMPLATES.items():
            req = ClientRequirementInput(
                project_name=t_data["project_name"],
                industry_domain=t_data["industry_domain"],
                problem_statement=t_data["problem_statement"],
                target_users=t_data["target_users"],
                expected_scale=t_data["expected_scale"],
                cloud_preference=t_data["cloud_preference"],
                compliance_needs=t_data["compliance_needs"]
            )
            blueprint = CynbitMultiAgentOrchestrator.execute_workflow(req)
            self.assertEqual(blueprint.project_name, t_data["project_name"])
            self.assertGreaterEqual(len(blueprint.microservices), 3)
            self.assertGreaterEqual(len(blueprint.agent_topology), 3)
            self.assertGreaterEqual(len(blueprint.security_audit), 4)
            self.assertEqual(len(blueprint.implementation_phases), 4)
            self.assertIn("Cynbit Technologies", blueprint.cynbit_value_proposition)


if __name__ == "__main__":
    unittest.main()
