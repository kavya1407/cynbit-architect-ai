"""
Cynbit ArchitectAI - Autonomous Solution Architecture & Agentic Workflow Engine
Built for Cynbit Technologies (cynbit.in)
AI/ML Engineer Intern Practical Assessment Deliverable
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from core.models import ClientRequirementInput
from core.agents import CynbitMultiAgentOrchestrator
from core.templates import SAMPLE_TEMPLATES
from core.cost_engine import CostEstimationEngine


# Page configuration
st.set_page_config(
    page_title="Cynbit ArchitectAI | Autonomous Solution Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling matching Cynbit's Dark Tech Theme
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
        padding: 24px 28px;
        border-radius: 12px;
        border: 1px solid #312E81;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .header-title {
        color: #38BDF8;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    
    .header-tagline {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 12px;
    }
    
    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
    }
    .pill-blue { background-color: #1E3A8A; color: #93C5FD; border: 1px solid #3B82F6; }
    .pill-emerald { background-color: #064E3B; color: #6EE7B7; border: 1px solid #10B981; }
    .pill-purple { background-color: #4C1D95; color: #D8B4FE; border: 1px solid #8B5CF6; }

    /* Card Box */
    .metric-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    
    .metric-val {
        color: #38BDF8;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .metric-lbl {
        color: #94A3B8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Agent Card */
    .agent-card {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 4px solid #38BDF8;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .agent-title {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .agent-role {
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    /* Security Alert Box */
    .sec-card-critical {
        background-color: #450A0A;
        border: 1px solid #991B1B;
        border-left: 5px solid #EF4444;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .sec-card-high {
        background-color: #431407;
        border: 1px solid #9A3412;
        border-left: 5px solid #F97316;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .sec-card-med {
        background-color: #172554;
        border: 1px solid #1E40AF;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


def render_mermaid(diagram_code: str, height: int = 420):
    """Renders a Mermaid.js diagram directly inside an HTML iframe."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'dark',
                themeVariables: {{
                    darkMode: true,
                    background: '#0B0F19',
                    primaryColor: '#1E293B',
                    primaryTextColor: '#F8FAFC',
                    primaryBorderColor: '#38BDF8',
                    lineColor: '#64748B',
                    secondaryColor: '#0F172A',
                    tertiaryColor: '#1E1B4B'
                }}
            }});
        </script>
        <style>
            body {{
                background-color: #0B0F19;
                margin: 0;
                padding: 10px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: -apple-system, sans-serif;
            }}
            .mermaid {{
                width: 100%;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
        {diagram_code}
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=height, scrolling=True)


# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80", width=60)
    st.markdown("### **Cynbit Technologies**")
    st.caption("AI/ML Engineer Intern Assessment")
    st.markdown("---")

    st.subheader("1. Load Scenario / Template")
    template_choices = ["Custom Architecture Brief"] + list(SAMPLE_TEMPLATES.keys())
    selected_template = st.selectbox("Select Benchmark Case Study", template_choices, index=1)

    # Defaults
    if selected_template != "Custom Architecture Brief":
        tpl_data = SAMPLE_TEMPLATES[selected_template]
        default_proj = tpl_data["project_name"]
        default_domain = tpl_data["industry_domain"]
        default_problem = tpl_data["problem_statement"].strip()
        default_target = tpl_data["target_users"]
        default_scale = tpl_data["expected_scale"]
        default_cloud = tpl_data["cloud_preference"]
    else:
        default_proj = "Custom AI Platform"
        default_domain = "Enterprise Operations"
        default_problem = "Describe your client workflow, multi-modal ingestion requirements, and operational bottlenecks here..."
        default_target = "Operations Team & Customers"
        default_scale = "Medium (10k - 100k MAU)"
        default_cloud = "GCP"

    st.markdown("---")
    st.subheader("2. Infrastructure & Model Setup")
    selected_cloud = st.selectbox("Cloud Preference", ["GCP", "AWS", "Azure", "Hybrid"], index=["GCP", "AWS", "Azure", "Hybrid"].index(default_cloud) if default_cloud in ["GCP", "AWS", "Azure", "Hybrid"] else 0)
    selected_scale = st.selectbox("Scale Tier", ["Small (< 10k MAU)", "Medium (10k - 100k MAU)", "High (100k - 1M MAU)", "Enterprise (> 1M MAU)"], index=["Small (< 10k MAU)", "Medium (10k - 100k MAU)", "High (100k - 1M MAU)", "Enterprise (> 1M MAU)"].index(default_scale) if default_scale in ["Small (< 10k MAU)", "Medium (10k - 100k MAU)", "High (100k - 1M MAU)", "Enterprise (> 1M MAU)"] else 1)
    selected_model = st.selectbox("Primary LLM Reasoning Engine", ["Gemini 2.0 Flash", "Gemini 1.5 Pro", "Claude 3.5 Sonnet", "GPT-4o-mini", "Open-Source (Llama 3.3 70B Self-Hosted vLLM)"], index=0)

    st.markdown("---")
    st.subheader("3. Optional LLM Key")
    user_api_key = st.text_input("Gemini / OpenAI API Key", type="password", help="Leave blank to use the deterministic offline synthesis engine (zero cost, 100% reliable)")
    if not user_api_key:
        st.markdown('<span class="pill pill-emerald">✓ Offline Heuristic Engine Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill pill-blue">✓ Live API Configured</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Cynbit Technologies Private Limited\nJaipur, Rajasthan, India\n[cynbit.in](https://cynbit.in)")


# ==========================================
# MAIN INTERACTION VIEW
# ==========================================

# Banner
st.markdown("""
<div class="header-box">
    <div class="header-title">⚡ Cynbit ArchitectAI</div>
    <div class="header-tagline">Autonomous Solution Architecture, Agentic Workflow Synthesis & Token Economics Engine</div>
    <div>
        <span class="pill pill-blue">Candidate: AI/ML Engineer Intern</span>
        <span class="pill pill-emerald">System: Multi-Agent Synthesis</span>
        <span class="pill pill-purple">Products: TenantEase • Revio • BitElevate • Studio</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section in an Expander
with st.expander("📝 Client Problem Statement & Technical Constraints", expanded=(selected_template == "Custom Architecture Brief")):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        proj_name = st.text_input("Project Name", value=default_proj)
        prob_stmt = st.text_area("Problem Statement / Client RFP Brief", value=default_problem, height=180)
    with col_b:
        domain_val = st.text_input("Industry Domain", value=default_domain)
        target_val = st.text_input("Target Users", value=default_target)
        compliance_vals = st.multiselect("Compliance Guardrails", ["GDPR", "SOC2-ready", "HIPAA", "FERPA-aligned", "Zero-Trust Data Isolation"], default=["GDPR", "SOC2-ready"])

# Run Button
generate_btn = st.button("🚀 Synthesize Architecture Blueprint & Agent DAG", type="primary", use_container_width=True)

# Execute Synthesis
req_obj = ClientRequirementInput(
    project_name=proj_name,
    industry_domain=domain_val,
    problem_statement=prob_stmt,
    target_users=target_val,
    expected_scale=selected_scale,
    cloud_preference=selected_cloud,
    compliance_needs=compliance_vals,
    budget_tier="Growth / Enterprise"
)

# Cache blueprint in session state so it survives slider interactions
if generate_btn or "blueprint" not in st.session_state:
    with st.spinner("Synthesizing multi-agent topology, cloud microservices, and token economics..."):
        blueprint = CynbitMultiAgentOrchestrator.execute_workflow(req_obj, model_choice=selected_model)
        st.session_state["blueprint"] = blueprint

blueprint = st.session_state["blueprint"]

# ==========================================
# DISPLAY BLUEPRINT
# ==========================================

# Executive Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Target Domain</div>
        <div class="metric-val" style="font-size: 1.25rem; color:#F8FAFC;">{blueprint.domain}</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Autonomous Agents</div>
        <div class="metric-val">{len(blueprint.agent_topology)}</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Microservice Layers</div>
        <div class="metric-val">{len(blueprint.microservices)}</div>
    </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Est. Monthly TCO</div>
        <div class="metric-val" style="color:#10B981;">${blueprint.token_economics.total_estimated_monthly_cost_usd:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📐 System Architecture",
    "🤖 Agentic Workflow DAG",
    "💰 Token Economics & TCO",
    "🛡️ OWASP Security Audit",
    "🚀 Execution Roadmap",
    "📄 Export Whitepaper"
])

# TAB 1: SYSTEM ARCHITECTURE
with tab1:
    st.subheader("High-Availability Microservices Topology")
    st.caption("Event-driven containerized architecture with zero-trust networking and API rate limiting.")
    
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        st.markdown("**Interactive Architecture Diagram (Mermaid.js)**")
        render_mermaid(blueprint.mermaid_architecture_code, height=440)
    with col_d2:
        st.markdown("**Executive Architecture Summary**")
        st.info(blueprint.executive_summary)
        
        st.markdown("**Production Tech Stack Specification**")
        for k, v in blueprint.recommended_tech_stack.items():
            st.markdown(f"- **{k}:** `{v}`")

    st.markdown("---")
    st.subheader("Microservice Node Breakdown")
    for s in blueprint.microservices:
        with st.expander(f"🔹 {s.name} ({s.layer})"):
            st.markdown(f"- **Underlying Technology:** `{s.technology}`")
            st.markdown(f"- **Functional Purpose:** {s.purpose}")
            st.markdown(f"- **Scaling Strategy:** {s.scaling_strategy}")

# TAB 2: AGENTIC WORKFLOW DAG
with tab2:
    st.subheader("Multi-Agent Cognitive Pipeline")
    st.caption("Specialized agent personas collaborating via typed state machines and tool calling.")
    
    st.markdown("**Agent Execution Directed Acyclic Graph (DAG)**")
    render_mermaid(blueprint.mermaid_agent_dag_code, height=280)
    
    st.markdown("---")
    st.subheader("Agent Persona & Tool Calling Directory")
    for a in blueprint.agent_topology:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-title">{a.name}</div>
            <div class="agent-role">Role: {a.role} &nbsp;|&nbsp; Assigned LLM: {a.llm_model}</div>
            <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">{a.primary_task}</p>
            <div style="font-size:0.85rem; color:#94A3B8;">
                <b>Tools:</b> {', '.join([f'<code>{t}</code>' for t in a.tools])}<br>
                <b>Input State:</b> {a.input_state}<br>
                <b>Output State:</b> {a.output_state}<br>
                <b>Fallback:</b> <span style="color:#F59E0B;">{a.fallback_strategy}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: TOKEN ECONOMICS & TCO
with tab3:
    st.subheader("Interactive Token Economics & Cloud Cost Modeling")
    st.caption("Fine-tune user volume, token lengths, and caching assumptions to project monthly operational expenditures.")

    c1, c2, c3 = st.columns(3)
    with c1:
        mau_slider = st.slider("Monthly Active Users (MAU)", min_value=1000, max_value=500000, value=blueprint.token_economics.monthly_active_users, step=5000)
    with c2:
        req_slider = st.slider("Monthly Requests per User", min_value=1, max_value=60, value=blueprint.token_economics.requests_per_user_month, step=1)
    with c3:
        cache_slider = st.slider("Semantic Cache Hit Ratio", min_value=0.0, max_value=0.70, value=0.30, step=0.05, format="%.2f")

    # Dynamic recalculation
    recalc = CostEstimationEngine.calculate_estimate(
        scale_tier=selected_scale,
        selected_model=selected_model,
        custom_mau=mau_slider,
        custom_reqs_per_user=req_slider,
        cache_hit_rate=cache_slider
    )

    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Total Monthly Requests", f"{mau_slider * req_slider:,}")
    with t2:
        st.metric("Input Tokens", f"{recalc.total_monthly_input_tokens_m:.1f} M")
    with t3:
        st.metric("Monthly LLM Inference", f"${recalc.monthly_llm_inference_cost_usd:,.2f}")
    with t4:
        st.metric("Total Monthly TCO", f"${recalc.total_estimated_monthly_cost_usd:,.2f}")

    st.markdown("---")
    st.subheader("Architectural Cost-Saving Strategies")
    for r in recalc.cost_saving_recommendations:
        st.markdown(f"💡 {r}")

# TAB 4: OWASP SECURITY AUDIT
with tab4:
    st.subheader("AI Security, Threat Modeling & Guardrails")
    st.caption("Evaluated against the OWASP Top 10 for Large Language Models (LLM01-LLM10).")

    for t in blueprint.security_audit:
        card_class = "sec-card-critical" if t.risk_level == "Critical" else ("sec-card-high" if t.risk_level == "High" else "sec-card-med")
        st.markdown(f"""
        <div class="{card_class}">
            <div style="font-weight:700; font-size:1.05rem; color:#F8FAFC;">
                {t.threat_category} &nbsp;
                <span class="pill {'pill-purple' if t.risk_level=='Critical' else 'pill-blue'}">{t.risk_level} Risk</span>
            </div>
            <p style="margin: 8px 0 6px 0; color:#E2E8F0; font-size:0.95rem;">{t.description}</p>
            <div style="font-size:0.88rem; color:#93C5FD;"><b>Mitigation Control:</b> {t.mitigation_strategy}</div>
        </div>
        """, unsafe_allow_html=True)

# TAB 5: EXECUTION ROADMAP
with tab5:
    st.subheader("Phased Implementation & Production Rollout Plan")
    st.caption("Standard 10-week enterprise execution sprint developed by Cynbit Technologies.")

    for p in blueprint.implementation_phases:
        with st.container():
            st.markdown(f"### {p['phase']}")
            st.markdown(f"**Key Deliverables:** `{p['deliverables']}`")
            for m in p["milestones"]:
                st.markdown(f"- {m}")
            st.markdown("")

    st.markdown("---")
    st.subheader("Cynbit Technologies' Value Proposition")
    st.success(blueprint.cynbit_value_proposition)

# TAB 6: EXPORT WHITEPAPER
with tab6:
    st.subheader("Export Technical Architecture Specification")
    st.caption("Download the synthesized architecture report as clean Markdown or copy JSON.")

    markdown_export = f"""# Technical Architecture Specification: {blueprint.project_name}
**Client Domain:** {blueprint.domain}  
**Architecture Pattern:** {blueprint.system_type}  
**Prepared for:** Cynbit Technologies Engineering Review  

## 1. Executive Summary
{blueprint.executive_summary}

## 2. Recommended Technology Stack
{chr(10).join([f"- **{k}:** {v}" for k, v in blueprint.recommended_tech_stack.items()])}

## 3. High-Availability Microservices Topology
{chr(10).join([f"### {s.name} ({s.layer})\n- **Tech:** {s.technology}\n- **Purpose:** {s.purpose}\n- **Scaling:** {s.scaling_strategy}" for s in blueprint.microservices])}

## 4. Multi-Agent Cognitive DAG
```mermaid
{blueprint.mermaid_agent_dag_code}
```

### Agent Directory
{chr(10).join([f"- **{a.name}** ({a.role}) | Model: {a.llm_model}\n  - Tasks: {a.primary_task}\n  - Tools: {', '.join(a.tools)}\n  - Fallback: {a.fallback_strategy}" for a in blueprint.agent_topology])}

## 5. Token Economics & Cost Modeling
- **Monthly Active Users:** {blueprint.token_economics.monthly_active_users:,}
- **Monthly Request Volume:** {blueprint.token_economics.monthly_active_users * blueprint.token_economics.requests_per_user_month:,}
- **Inference Model:** {blueprint.token_economics.selected_model}
- **Monthly LLM Inference Cost:** ${blueprint.token_economics.monthly_llm_inference_cost_usd:,.2f} USD
- **Monthly Cloud Infrastructure:** ${blueprint.token_economics.monthly_cloud_infra_cost_usd:,.2f} USD
- **Total Projected Monthly TCO:** ${blueprint.token_economics.total_estimated_monthly_cost_usd:,.2f} USD

## 6. OWASP LLM Security Audit & Mitigation
{chr(10).join([f"### {t.threat_category} [{t.risk_level} Risk]\n- **Threat:** {t.description}\n- **Mitigation:** {t.mitigation_strategy}" for t in blueprint.security_audit])}

## 7. Execution Roadmap
{chr(10).join([f"### {p['phase']}\n- Deliverables: {p['deliverables']}\n" + chr(10).join([f"  - {m}" for m in p['milestones']]) for p in blueprint.implementation_phases])}

## 8. Strategic Value Proposition
{blueprint.cynbit_value_proposition}
"""

    st.download_button(
        label="📥 Download Complete Architecture Specification (.md)",
        data=markdown_export,
        file_name=f"{blueprint.project_name.lower().replace(' ', '_')}_spec.md",
        mime="text/markdown",
        use_container_width=True
    )

    with st.expander("View Raw Specification Markdown"):
        st.code(markdown_export, language="markdown")
