"""
Command-Line Interface (CLI) for Cynbit ArchitectAI.
Allows rapid synthesis of architecture blueprints and cost estimates from the terminal.
"""

import argparse
import sys
import os
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.models import ClientRequirementInput
from core.agents import CynbitMultiAgentOrchestrator
from core.templates import SAMPLE_TEMPLATES
from core.cost_engine import CostEstimationEngine


def main():
    parser = argparse.ArgumentParser(
        description="Cynbit ArchitectAI CLI - Autonomous Architecture & Agentic Workflow Engine"
    )
    parser.add_argument("--template", type=str, choices=list(SAMPLE_TEMPLATES.keys()), help="Name of pre-configured case study")
    parser.add_argument("--project", type=str, default="Cynbit Custom System", help="Project name")
    parser.add_argument("--domain", type=str, default="Enterprise Operations", help="Industry domain")
    parser.add_argument("--problem", type=str, help="Problem statement or client brief")
    parser.add_argument("--scale", type=str, default="Medium (10k - 100k MAU)", help="Traffic scale tier")
    parser.add_argument("--cloud", type=str, default="GCP", help="Preferred cloud provider (GCP, AWS, Azure)")
    parser.add_argument("--model", type=str, default="Gemini 2.0 Flash", help="LLM model choice")
    parser.add_argument("--output", type=str, help="Path to save synthesized Markdown specification")

    args = parser.parse_args()

    print("=" * 70)
    print(">> CYNBIT ARCHITECTAI - AUTONOMOUS SOLUTION ENGINE")
    print("   Cynbit Technologies Private Limited (Jaipur, India)")
    print("=" * 70)

    if args.template:
        print(f"[*] Loading pre-configured template: {args.template}")
        t_data = SAMPLE_TEMPLATES[args.template]
        req = ClientRequirementInput(
            project_name=t_data["project_name"],
            industry_domain=t_data["industry_domain"],
            problem_statement=t_data["problem_statement"],
            target_users=t_data["target_users"],
            expected_scale=t_data["expected_scale"],
            cloud_preference=t_data["cloud_preference"],
            compliance_needs=t_data["compliance_needs"]
        )
    elif args.problem:
        req = ClientRequirementInput(
            project_name=args.project,
            industry_domain=args.domain,
            problem_statement=args.problem,
            expected_scale=args.scale,
            cloud_preference=args.cloud
        )
    else:
        print("[!] No problem statement or template provided. Defaulting to 'TenantEase AI' benchmark.")
        t_data = SAMPLE_TEMPLATES["TenantEase AI (PropTech Maintenance & Lease Agent)"]
        req = ClientRequirementInput(
            project_name=t_data["project_name"],
            industry_domain=t_data["industry_domain"],
            problem_statement=t_data["problem_statement"],
            target_users=t_data["target_users"],
            expected_scale=t_data["expected_scale"],
            cloud_preference=t_data["cloud_preference"],
            compliance_needs=t_data["compliance_needs"]
        )

    print(f"[*] Analyzing requirements for: '{req.project_name}' ({req.industry_domain})...")
    blueprint = CynbitMultiAgentOrchestrator.execute_workflow(req, model_choice=args.model)

    print("\n[+] SYNTHESIS COMPLETE!")
    print(f"    - System Type: {blueprint.system_type}")
    print(f"    - Microservices Layers: {len(blueprint.microservices)}")
    print(f"    - Autonomous Agents: {len(blueprint.agent_topology)}")
    print(f"    - Est. Monthly TCO: ${blueprint.token_economics.total_estimated_monthly_cost_usd:,.2f} USD")
    print(f"      (Inference: ${blueprint.token_economics.monthly_llm_inference_cost_usd:.2f} | Infra: ${blueprint.token_economics.monthly_cloud_infra_cost_usd:.2f})")

    print("\n--- RECOMMENDED TECH STACK ---")
    for k, v in blueprint.recommended_tech_stack.items():
        print(f"  {k:25}: {v}")

    print("\n--- AGENTIC WORKFLOW TOPOLOGY ---")
    for a in blueprint.agent_topology:
        print(f"  * {a.name} ({a.role}) -> Model: {a.llm_model}")
        print(f"    Tools: {', '.join(a.tools)}")

    print("\n--- OWASP SECURITY AUDIT ---")
    for t in blueprint.security_audit:
        print(f"  [{t.risk_level.upper()}] {t.threat_category}: {t.mitigation_strategy[:65]}...")

    if args.output:
        md_text = f"# Architecture Specification: {blueprint.project_name}\n\n{blueprint.executive_summary}\n\n## Mermaid Diagram\n```mermaid\n{blueprint.mermaid_architecture_code}\n```"
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"\n[SUCCESS] Specification successfully written to: {args.output}")

    print("=" * 70)


if __name__ == "__main__":
    main()
