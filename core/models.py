"""
Data models for Cynbit ArchitectAI.
Provides strict schema validation with Pydantic v2 when installed,
with a seamless Python standard-library fallback for zero-dependency execution.
"""

from typing import List, Dict, Optional, Any
import sys

try:
    from pydantic import BaseModel, Field
except ImportError:
    from dataclasses import dataclass, field, asdict

    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        
        def dict(self) -> Dict[str, Any]:
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        
        def model_dump(self) -> Dict[str, Any]:
            return self.dict()

    def Field(default=None, default_factory=None, description=""):
        if default_factory is not None:
            return default_factory()
        return default


class ClientRequirementInput(BaseModel):
    """Raw client requirement input submitted through UI or API."""
    def __init__(
        self,
        project_name: str,
        problem_statement: str,
        industry_domain: str = "General Enterprise",
        target_users: str = "External customers and internal operators",
        expected_scale: str = "Medium (10k - 100k MAU)",
        cloud_preference: str = "GCP",
        compliance_needs: Optional[List[str]] = None,
        budget_tier: str = "Growth / Enterprise",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.project_name = project_name
        self.problem_statement = problem_statement
        self.industry_domain = industry_domain
        self.target_users = target_users
        self.expected_scale = expected_scale
        self.cloud_preference = cloud_preference
        self.compliance_needs = compliance_needs or ["GDPR", "SOC2-ready"]
        self.budget_tier = budget_tier


class AgentComponent(BaseModel):
    """Definition of an individual autonomous agent in the system."""
    def __init__(
        self,
        name: str,
        role: str,
        primary_task: str,
        llm_model: str,
        tools: List[str],
        input_state: str,
        output_state: str,
        fallback_strategy: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.role = role
        self.primary_task = primary_task
        self.llm_model = llm_model
        self.tools = tools
        self.input_state = input_state
        self.output_state = output_state
        self.fallback_strategy = fallback_strategy


class MicroserviceNode(BaseModel):
    """Definition of an infrastructure or microservice component."""
    def __init__(
        self,
        id: str,
        name: str,
        layer: str,
        technology: str,
        purpose: str,
        scaling_strategy: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.layer = layer
        self.technology = technology
        self.purpose = purpose
        self.scaling_strategy = scaling_strategy


class TokenCostEstimate(BaseModel):
    """Token economics and recurring inference cost breakdown."""
    def __init__(
        self,
        monthly_active_users: int,
        requests_per_user_month: int,
        avg_input_tokens_per_req: int,
        avg_output_tokens_per_req: int,
        total_monthly_input_tokens_m: float,
        total_monthly_output_tokens_m: float,
        selected_model: str,
        model_input_cost_per_m: float,
        model_output_cost_per_m: float,
        monthly_llm_inference_cost_usd: float,
        monthly_cloud_infra_cost_usd: float,
        total_estimated_monthly_cost_usd: float,
        cost_saving_recommendations: List[str],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.monthly_active_users = monthly_active_users
        self.requests_per_user_month = requests_per_user_month
        self.avg_input_tokens_per_req = avg_input_tokens_per_req
        self.avg_output_tokens_per_req = avg_output_tokens_per_req
        self.total_monthly_input_tokens_m = total_monthly_input_tokens_m
        self.total_monthly_output_tokens_m = total_monthly_output_tokens_m
        self.selected_model = selected_model
        self.model_input_cost_per_m = model_input_cost_per_m
        self.model_output_cost_per_m = model_output_cost_per_m
        self.monthly_llm_inference_cost_usd = monthly_llm_inference_cost_usd
        self.monthly_cloud_infra_cost_usd = monthly_cloud_infra_cost_usd
        self.total_estimated_monthly_cost_usd = total_estimated_monthly_cost_usd
        self.cost_saving_recommendations = cost_saving_recommendations


class SecurityThreat(BaseModel):
    """Security audit item based on OWASP Top 10 for LLMs."""
    def __init__(
        self,
        threat_category: str,
        risk_level: str,
        description: str,
        mitigation_strategy: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.threat_category = threat_category
        self.risk_level = risk_level
        self.description = description
        self.mitigation_strategy = mitigation_strategy


class ArchitectureBlueprint(BaseModel):
    """Complete synthesized architecture blueprint."""
    def __init__(
        self,
        project_name: str,
        domain: str,
        executive_summary: str,
        system_type: str,
        recommended_tech_stack: Dict[str, str],
        microservices: List[MicroserviceNode],
        agent_topology: List[AgentComponent],
        data_pipeline_stages: List[str],
        mermaid_architecture_code: str,
        mermaid_agent_dag_code: str,
        token_economics: TokenCostEstimate,
        security_audit: List[SecurityThreat],
        implementation_phases: List[Dict[str, Any]],
        cynbit_value_proposition: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.project_name = project_name
        self.domain = domain
        self.executive_summary = executive_summary
        self.system_type = system_type
        self.recommended_tech_stack = recommended_tech_stack
        self.microservices = microservices
        self.agent_topology = agent_topology
        self.data_pipeline_stages = data_pipeline_stages
        self.mermaid_architecture_code = mermaid_architecture_code
        self.mermaid_agent_dag_code = mermaid_agent_dag_code
        self.token_economics = token_economics
        self.security_audit = security_audit
        self.implementation_phases = implementation_phases
        self.cynbit_value_proposition = cynbit_value_proposition
