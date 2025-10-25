import plotly.express as px
import pandas as pd

def create_energy_distribution_pie(self_used, excess, deficit):
    fig = px.pie(
        values=[self_used, excess, deficit],
        names=["Self-Consumed", "Excess Sold", "Deficit"],
        title="Monthly Energy Distribution",
    )
    return fig

def create_monthly_financial_bar(savings, income, cost, net_benefit):
    df = pd.DataFrame({
        "Category": ["Savings", "Income", "Cost", "Net Benefit"],
        "Amount": [savings, income, cost, net_benefit]
    })
    fig = px.bar(df, x="Category", y="Amount", title="Monthly Financial Breakdown")
    return fig

def create_roi_comparison_bar(subsidy_levels, roi_values):
    df = pd.DataFrame({"Subsidy (%)": subsidy_levels, "ROI (%)": roi_values})
    fig = px.bar(df, x="Subsidy (%)", y="ROI (%)", text="ROI (%)", title="ROI Comparison by Subsidy Level")
    return fig
