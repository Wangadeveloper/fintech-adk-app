import pandas as pd
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

# --- 1. TOOL DEFINITIONS ---

def analyze_mpesa_data() -> dict:
    """Loads and performs raw calculations on M-Pesa transaction data."""
    # Simulating data loading and cleaning logic from your provided code
    # In a real scenario, this would read from your /tmp/mpesa.csv
    return {
        "income_total": 58500.0,
        "withdrawal_total": 61350.0,
        "net_cashflow": -2850.0,
        "top_spending": {"Bills": 15000, "Loans": 14500},
        "days_in_overdraft": 4
    }

# --- 2. SPECIALIZED AGENT DEFINITIONS ---

# Agent 1: Handles data retrieval and cleaning [cite: 724]
data_ingestion_agent = Agent(
    name="DataIngestionAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Use the 'analyze_mpesa_data' tool to extract raw financial metrics. 
    Provide the raw numbers without advice.""",
    tools=[analyze_mpesa_data],
    output_key="raw_financial_data"
)

# Agent 2: Focuses on spending patterns and cash flow [cite: 724]
financial_analyst_agent = Agent(
    name="FinancialAnalystAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Analyze these raw metrics: {raw_financial_data}. 
    Focus on spending profile and cashflow stability. 
    Identify if spending exceeds income.""",
    output_key="analyst_report"
)

# Agent 3: Final step to assess creditworthiness and give advice [cite: 724]
risk_advisor_agent = Agent(
    name="RiskAdvisorAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Review the analyst report: {analyst_report}. 
    Provide a final financial score (e.g., 580/800), a specific loan recommendation 
    (Approve/Refuse), and actionable advice to improve liquidity.""",
    output_key="final_insights"
)

# --- 3. SEQUENTIAL AGENT (ROOT) ---

# This replaces the A2A structure with a local "Assembly Line" [cite: 404, 446]
root_agent = SequentialAgent(
    name="MpesaInsightPipeline",
    description="A sequential pipeline for M-Pesa financial assessment.",
    # The agents run in the exact order listed here [cite: 477]
    sub_agents=[
        data_ingestion_agent, 
        financial_analyst_agent, 
        risk_advisor_agent
    ]
)

print("✅ Sequential M-Pesa Insight Agent created successfully.")