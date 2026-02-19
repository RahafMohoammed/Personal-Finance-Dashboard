import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Personal Finance Behavioral Analysis Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════
# CUSTOM CSS FOR PROFESSIONAL STYLING
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    .main { padding-top: 0.5rem; }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .stMetric label { color: white !important; font-weight: 600; }
    .stMetric [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 26px !important; }
    .stMetric [data-testid="stMetricDelta"] { color: #90EE90 !important; }
    h1 { color: #1a1a2e; font-weight: 800; }
    h2 { color: #16213e; font-weight: 700; }
    h3 { color: #0f3460; font-weight: 600; }
    .insight-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #1976d2;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# DATA LOADING & PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    """Load and preprocess the personal finance dataset"""
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    
    # Convert date column
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    
    # Create derived metrics
    df["net_cash_flow"] = df["monthly_income"] - df["monthly_expense_total"]
    df["expense_to_income_ratio"] = (df["monthly_expense_total"] / df["monthly_income"]).round(2)
    df["loan_burden_pct"] = (df["loan_payment"] / df["monthly_income"] * 100).round(1)
    
    # Credit score bands
    def credit_band(score):
        if score <= 579:
            return "Poor (≤579)"
        elif score <= 669:
            return "Fair (580-669)"
        elif score <= 739:
            return "Good (670-739)"
        elif score <= 799:
            return "Very Good (740-799)"
        else:
            return "Exceptional (800+)"
    
    df["credit_band"] = df["credit_score"].apply(credit_band)
    
    return df

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Dataset file not found. Please ensure 'personal_finance_tracker_dataset.csv' is in the same directory as this script.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💰 Personal Finance Behavioral Analysis Dashboard")
    st.markdown("**Comprehensive analysis of spending patterns, savings behavior, and financial health across economic scenarios**")
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Finance_and_Banking.svg/200px-Finance_and_Banking.svg.png", width=100)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════════════
st.sidebar.title("🔍 Filter Dashboard")
st.sidebar.markdown("**Customize your analysis view**")
st.sidebar.markdown("---")

# Year filter
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect(
    "📅 Select Years",
    options=years,
    default=years
)

# Economic scenario filter
scenarios = sorted(df["financial_scenario"].unique())
selected_scenarios = st.sidebar.multiselect(
    "🌐 Economic Scenario",
    options=scenarios,
    default=scenarios
)

# Income type filter
income_types = sorted(df["income_type"].unique())
selected_income_types = st.sidebar.multiselect(
    "💼 Income Type",
    options=income_types,
    default=income_types
)

# Stress level filter
stress_levels = ["Low", "Medium", "High"]
selected_stress = st.sidebar.multiselect(
    "😰 Financial Stress Level",
    options=stress_levels,
    default=stress_levels
)

# Category filter
categories = sorted(df["category"].unique())
selected_categories = st.sidebar.multiselect(
    "🏷️ Spending Category",
    options=categories,
    default=categories
)

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Dataset Overview**
- 📊 Total Records: {len(df):,}
- 👥 Unique Users: {df['user_id'].nunique():,}
- 📅 Period: 2019-2023
- 🌐 Data Source: Kaggle
""")

# Apply filters
filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["financial_scenario"].isin(selected_scenarios)) &
    (df["income_type"].isin(selected_income_types)) &
    (df["financial_stress_level"].isin(selected_stress)) &
    (df["category"].isin(selected_categories))
]

if filtered_df.empty:
    st.warning("⚠️ No data matches your filter selection. Please adjust filters.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# KEY PERFORMANCE INDICATORS (KPIs)
# ═══════════════════════════════════════════════════════════════════════
st.subheader("📊 Key Financial Metrics")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    avg_income = filtered_df["monthly_income"].mean()
    st.metric(
        label="Avg Monthly Income",
        value=f"${avg_income:,.0f}",
        delta=f"{((avg_income - df['monthly_income'].mean()) / df['monthly_income'].mean() * 100):.1f}% vs overall"
    )

with kpi2:
    avg_expense = filtered_df["monthly_expense_total"].mean()
    st.metric(
        label="Avg Monthly Expenses",
        value=f"${avg_expense:,.0f}",
        delta=f"{((avg_expense - df['monthly_expense_total'].mean()) / df['monthly_expense_total'].mean() * 100):.1f}% vs overall"
    )

with kpi3:
    avg_savings = filtered_df["actual_savings"].mean()
    st.metric(
        label="Avg Actual Savings",
        value=f"${avg_savings:,.0f}",
        delta=f"{filtered_df['savings_rate'].mean()*100:.1f}% savings rate"
    )

with kpi4:
    goal_met_rate = filtered_df["savings_goal_met"].mean() * 100
    st.metric(
        label="Savings Goal Met",
        value=f"{goal_met_rate:.1f}%",
        delta=f"{len(filtered_df[filtered_df['savings_goal_met']==1]):,} users"
    )

with kpi5:
    avg_credit = filtered_df["credit_score"].mean()
    st.metric(
        label="Avg Credit Score",
        value=f"{avg_credit:.0f}",
        delta="Good range" if avg_credit >= 670 else "Fair range"
    )

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════
# TAB NAVIGATION
# ═══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Income & Expenses Analysis",
    "💰 Savings Behavior",
    "🌐 Economic Scenarios Comparison",
    "📋 Credit & Debt Profile",
    "🔍 Behavioral Insights"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: INCOME & EXPENSES ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    st.header("📈 Income & Expenses Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Yearly trend
        st.subheader("Year-over-Year Trend")
        yearly_data = filtered_df.groupby("year").agg({
            "monthly_income": "mean",
            "monthly_expense_total": "mean",
            "actual_savings": "mean"
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly_data["year"], y=yearly_data["monthly_income"],
            mode="lines+markers", name="Income",
            line=dict(color="#2ecc71", width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=yearly_data["year"], y=yearly_data["monthly_expense_total"],
            mode="lines+markers", name="Expenses",
            line=dict(color="#e74c3c", width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=yearly_data["year"], y=yearly_data["actual_savings"],
            mode="lines+markers", name="Savings",
            line=dict(color="#3498db", width=3, dash="dot"),
            marker=dict(size=10)
        ))
        fig.update_layout(
            height=400,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis_title="Year",
            yaxis_title="Amount ($)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Income type distribution
        st.subheader("Income Type Distribution")
        income_dist = filtered_df.groupby("income_type")["monthly_income"].mean().reset_index()
        
        fig2 = px.bar(
            income_dist,
            x="income_type",
            y="monthly_income",
            color="income_type",
            color_discrete_map={
                "Salary": "#2ecc71",
                "Freelance": "#e67e22",
                "Mixed": "#9b59b6"
            },
            text=income_dist["monthly_income"].apply(lambda x: f"${x:,.0f}"),
            labels={"monthly_income": "Avg Monthly Income ($)", "income_type": "Income Type"}
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            height=400,
            showlegend=False,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Spending by category
        st.subheader("Average Spending by Category")
        cat_spending = filtered_df.groupby("category").agg({
            "essential_spending": "mean",
            "discretionary_spending": "mean"
        }).reset_index().sort_values("essential_spending", ascending=True)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=cat_spending["category"],
            x=cat_spending["essential_spending"],
            name="Essential",
            orientation="h",
            marker_color="#3498db"
        ))
        fig3.add_trace(go.Bar(
            y=cat_spending["category"],
            x=cat_spending["discretionary_spending"],
            name="Discretionary",
            orientation="h",
            marker_color="#f39c12"
        ))
        fig3.update_layout(
            barmode="stack",
            height=400,
            xaxis_title="Average Amount ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            template="plotly_white"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Cash flow status
        st.subheader("Cash Flow Status Distribution")
        cash_flow = filtered_df["cash_flow_status"].value_counts().reset_index()
        cash_flow.columns = ["Status", "Count"]
        
        fig4 = px.pie(
            cash_flow,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map={
                "Positive": "#2ecc71",
                "Neutral": "#f39c12",
                "Negative": "#e74c3c"
            },
            hole=0.4
        )
        fig4.update_traces(textinfo="percent+label", textfont_size=13)
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: SAVINGS BEHAVIOR
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    st.header("💰 Savings Behavior Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Savings rate distribution
        st.subheader("Savings Rate Distribution")
        fig5 = px.histogram(
            filtered_df,
            x="savings_rate",
            nbins=40,
            color_discrete_sequence=["#3498db"],
            labels={"savings_rate": "Savings Rate", "count": "Number of Records"}
        )
        fig5.add_vline(
            x=filtered_df["savings_rate"].mean(),
            line_dash="dash",
            line_color="#e74c3c",
            annotation_text=f"Mean: {filtered_df['savings_rate'].mean():.2%}",
            annotation_position="top right"
        )
        fig5.update_layout(height=350, template="plotly_white")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Savings goal achievement by year
        st.subheader("Savings Goal Achievement Rate")
        goal_by_year = filtered_df.groupby("year")["savings_goal_met"].mean().reset_index()
        goal_by_year["percentage"] = goal_by_year["savings_goal_met"] * 100
        
        fig6 = px.bar(
            goal_by_year,
            x="year",
            y="percentage",
            color="percentage",
            color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
            text=goal_by_year["percentage"].apply(lambda x: f"{x:.1f}%"),
            labels={"percentage": "Goal Met (%)", "year": "Year"}
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(height=350, showlegend=False, template="plotly_white")
        st.plotly_chart(fig6, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Actual savings by stress level
        st.subheader("Savings by Stress Level & Income Type")
        savings_stress = filtered_df.groupby(["financial_stress_level", "income_type"])["actual_savings"].mean().reset_index()
        
        fig7 = px.bar(
            savings_stress,
            x="financial_stress_level",
            y="actual_savings",
            color="income_type",
            barmode="group",
            color_discrete_map={
                "Salary": "#2ecc71",
                "Freelance": "#e67e22",
                "Mixed": "#9b59b6"
            },
            category_orders={"financial_stress_level": ["Low", "Medium", "High"]},
            labels={"actual_savings": "Avg Actual Savings ($)"}
        )
        fig7.update_layout(height=350, template="plotly_white")
        st.plotly_chart(fig7, use_container_width=True)
    
    with col4:
        # Emergency fund vs actual savings
        st.subheader("Emergency Fund vs Actual Savings")
        sample = filtered_df.sample(min(500, len(filtered_df)), random_state=42)
        
        fig8 = px.scatter(
            sample,
            x="emergency_fund",
            y="actual_savings",
            color="cash_flow_status",
            color_discrete_map={
                "Positive": "#2ecc71",
                "Neutral": "#f39c12",
                "Negative": "#e74c3c"
            },
            opacity=0.6,
            trendline="ols",
            labels={"emergency_fund": "Emergency Fund ($)", "actual_savings": "Actual Savings ($)"}
        )
        fig8.update_layout(height=350, template="plotly_white")
        st.plotly_chart(fig8, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: ECONOMIC SCENARIOS COMPARISON
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.header("🌐 Economic Scenarios Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Metrics by scenario
        st.subheader("Financial Metrics Across Scenarios")
        scenario_metrics = filtered_df.groupby("financial_scenario").agg({
            "monthly_income": "mean",
            "monthly_expense_total": "mean",
            "actual_savings": "mean"
        }).reset_index()
        
        fig9 = go.Figure()
        fig9.add_trace(go.Bar(
            x=scenario_metrics["financial_scenario"],
            y=scenario_metrics["monthly_income"],
            name="Income",
            marker_color="#2ecc71"
        ))
        fig9.add_trace(go.Bar(
            x=scenario_metrics["financial_scenario"],
            y=scenario_metrics["monthly_expense_total"],
            name="Expenses",
            marker_color="#e74c3c"
        ))
        fig9.add_trace(go.Bar(
            x=scenario_metrics["financial_scenario"],
            y=scenario_metrics["actual_savings"],
            name="Savings",
            marker_color="#3498db"
        ))
        fig9.update_layout(
            barmode="group",
            height=370,
            yaxis_title="Amount ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            template="plotly_white"
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # Stress distribution by scenario
        st.subheader("Stress Level Distribution by Scenario")
        stress_scenario = filtered_df.groupby(["financial_scenario", "financial_stress_level"]).size().unstack(fill_value=0)
        stress_scenario_pct = stress_scenario.div(stress_scenario.sum(axis=1), axis=0) * 100
        
        fig10 = go.Figure()
        for stress in ["Low", "Medium", "High"]:
            if stress in stress_scenario_pct.columns:
                fig10.add_trace(go.Bar(
                    x=stress_scenario_pct.index,
                    y=stress_scenario_pct[stress],
                    name=stress,
                    marker_color={"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"}[stress]
                ))
        fig10.update_layout(
            barmode="stack",
            height=370,
            yaxis_title="Percentage (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            template="plotly_white"
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Debt-to-income by scenario
        st.subheader("Debt-to-Income Ratio by Scenario")
        fig11 = px.box(
            filtered_df,
            x="financial_scenario",
            y="debt_to_income_ratio",
            color="financial_scenario",
            color_discrete_map={
                "normal": "#3498db",
                "inflation": "#e67e22",
                "recession": "#e74c3c"
            },
            labels={"debt_to_income_ratio": "Debt-to-Income Ratio"}
        )
        fig11.update_layout(height=340, showlegend=False, template="plotly_white")
        st.plotly_chart(fig11, use_container_width=True)
    
    with col4:
        # Investment by scenario
        st.subheader("Investment Activity by Scenario")
        inv_scenario = filtered_df.groupby(["financial_scenario", "income_type"])["investment_amount"].mean().reset_index()
        
        fig12 = px.bar(
            inv_scenario,
            x="financial_scenario",
            y="investment_amount",
            color="income_type",
            barmode="group",
            color_discrete_map={
                "Salary": "#2ecc71",
                "Freelance": "#e67e22",
                "Mixed": "#9b59b6"
            },
            labels={"investment_amount": "Avg Investment ($)"}
        )
        fig12.update_layout(height=340, template="plotly_white")
        st.plotly_chart(fig12, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 4: CREDIT & DEBT PROFILE
# ═══════════════════════════════════════════════════════════════════════
with tab4:
    st.header("📋 Credit & Debt Profile Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Credit score distribution
        st.subheader("Credit Score Distribution")
        fig13 = px.histogram(
            filtered_df,
            x="credit_score",
            nbins=40,
            color_discrete_sequence=["#667eea"],
            labels={"credit_score": "Credit Score", "count": "Count"}
        )
        fig13.add_vline(x=670, line_dash="dash", line_color="#e74c3c",
                        annotation_text="Good (670)", annotation_position="top")
        fig13.add_vline(x=740, line_dash="dash", line_color="#2ecc71",
                        annotation_text="Very Good (740)", annotation_position="top")
        fig13.update_layout(height=350, template="plotly_white")
        st.plotly_chart(fig13, use_container_width=True)
    
    with col2:
        # Credit band breakdown
        st.subheader("Credit Score Band Distribution")
        band_counts = filtered_df["credit_band"].value_counts().reset_index()
        band_counts.columns = ["Band", "Count"]
        
        fig14 = px.pie(
            band_counts,
            names="Band",
            values="Count",
            color="Band",
            color_discrete_map={
                "Poor (≤579)": "#c0392b",
                "Fair (580-669)": "#e67e22",
                "Good (670-739)": "#f1c40f",
                "Very Good (740-799)": "#27ae60",
                "Exceptional (800+)": "#1abc9c"
            },
            hole=0.4
        )
        fig14.update_traces(textinfo="percent+label")
        fig14.update_layout(height=350)
        st.plotly_chart(fig14, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Debt vs credit score
        st.subheader("Debt-to-Income vs Credit Score")
        sample2 = filtered_df.sample(min(600, len(filtered_df)), random_state=7)
        
        fig15 = px.scatter(
            sample2,
            x="debt_to_income_ratio",
            y="credit_score",
            color="cash_flow_status",
            color_discrete_map={
                "Positive": "#2ecc71",
                "Neutral": "#f39c12",
                "Negative": "#e74c3c"
            },
            opacity=0.6,
            trendline="ols",
            labels={"debt_to_income_ratio": "Debt-to-Income Ratio"}
        )
        fig15.update_layout(height=340, template="plotly_white")
        st.plotly_chart(fig15, use_container_width=True)
    
    with col4:
        # Loan burden by income type
        st.subheader("Loan Payment Burden by Income Type")
        loan_data = filtered_df[filtered_df["loan_payment"] > 0]
        
        fig16 = px.box(
            loan_data,
            x="income_type",
            y="loan_burden_pct",
            color="income_type",
            color_discrete_map={
                "Salary": "#2ecc71",
                "Freelance": "#e67e22",
                "Mixed": "#9b59b6"
            },
            labels={"loan_burden_pct": "Loan as % of Income"}
        )
        fig16.update_layout(height=340, showlegend=False, template="plotly_white")
        st.plotly_chart(fig16, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 5: BEHAVIORAL INSIGHTS
# ═══════════════════════════════════════════════════════════════════════
with tab5:
    st.header("🔍 Behavioral Insights & Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Financial advice score
        st.subheader("Financial Advice Score by Stress Level")
        advice_stress = filtered_df.groupby("financial_stress_level")["financial_advice_score"].mean().reset_index()
        
        fig17 = px.bar(
            advice_stress,
            x="financial_stress_level",
            y="financial_advice_score",
            color="financial_stress_level",
            color_discrete_map={
                "Low": "#2ecc71",
                "Medium": "#f39c12",
                "High": "#e74c3c"
            },
            text=advice_stress["financial_advice_score"].apply(lambda x: f"{x:.1f}"),
            category_orders={"financial_stress_level": ["Low", "Medium", "High"]},
            labels={"financial_advice_score": "Avg Advice Score"}
        )
        fig17.update_traces(textposition="outside")
        fig17.update_layout(height=340, showlegend=False, template="plotly_white")
        st.plotly_chart(fig17, use_container_width=True)
    
    with col2:
        # Fraud analysis
        st.subheader("Fraud Rate by Category & Scenario")
        fraud_data = filtered_df.groupby(["category", "financial_scenario"])["fraud_flag"].mean().reset_index()
        fraud_data["fraud_pct"] = fraud_data["fraud_flag"] * 100
        
        fig18 = px.density_heatmap(
            fraud_data,
            x="financial_scenario",
            y="category",
            z="fraud_pct",
            color_continuous_scale="Reds",
            labels={"fraud_pct": "Fraud Rate (%)"}
        )
        fig18.update_layout(height=340, template="plotly_white")
        st.plotly_chart(fig18, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Subscription impact
        st.subheader("Subscription Services vs Discretionary Spending")
        sub_spending = filtered_df.groupby("subscription_services")["discretionary_spending"].mean().reset_index()
        
        fig19 = px.bar(
            sub_spending,
            x="subscription_services",
            y="discretionary_spending",
            color="discretionary_spending",
            color_continuous_scale="Blues",
            labels={
                "subscription_services": "Number of Subscriptions",
                "discretionary_spending": "Avg Discretionary Spending ($)"
            }
        )
        fig19.update_layout(height=340, showlegend=False, template="plotly_white")
        st.plotly_chart(fig19, use_container_width=True)
    
    with col4:
        # Net cash flow trend
        st.subheader("Net Cash Flow Trend by Scenario")
        ncf_trend = filtered_df.groupby(["year", "financial_scenario"])["net_cash_flow"].mean().reset_index()
        
        fig20 = px.line(
            ncf_trend,
            x="year",
            y="net_cash_flow",
            color="financial_scenario",
            color_discrete_map={
                "normal": "#3498db",
                "inflation": "#e67e22",
                "recession": "#e74c3c"
            },
            markers=True,
            labels={"net_cash_flow": "Avg Net Cash Flow ($)"}
        )
        fig20.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
        fig20.update_layout(height=340, template="plotly_white")
        st.plotly_chart(fig20, use_container_width=True)
    
    # Key Insights
    st.markdown("---")
    st.subheader("💡 Key Insights from Behavioral Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <strong>📊 Savings Goal Achievement</strong><br>
        Only <strong>{filtered_df['savings_goal_met'].mean()*100:.1f}%</strong> of users meet their savings goals, 
        despite {(filtered_df['cash_flow_status']=='Positive').mean()*100:.1f}% having positive cash flow. 
        This suggests goal-setting misalignment or behavioral spending patterns.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recession_savings = filtered_df[filtered_df["financial_scenario"]=="recession"]["actual_savings"].mean()
        normal_savings = filtered_df[filtered_df["financial_scenario"]=="normal"]["actual_savings"].mean()
        st.markdown(f"""
        <div class="insight-box">
        <strong>🌐 Economic Impact</strong><br>
        Recession periods reduce average savings by <strong>${normal_savings - recession_savings:,.0f}</strong> compared to 
        normal conditions. {(filtered_df[filtered_df['financial_scenario']=='recession']['financial_stress_level']=='High').mean()*100:.0f}% 
        of recession-period users report high stress.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        fraud_rate = filtered_df["fraud_flag"].mean() * 100
        st.markdown(f"""
        <div class="insight-box">
        <strong>🚨 Fraud & Risk</strong><br>
        Fraud incidents occur in <strong>{fraud_rate:.2f}%</strong> of records, with higher concentration 
        during inflation periods. Subscription count correlates positively with discretionary spending vulnerability.
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# DATA TABLE (EXPANDABLE)
# ═══════════════════════════════════════════════════════════════════════
st.markdown("---")
with st.expander("📋 View Filtered Raw Data"):
    display_columns = [
        "date", "user_id", "monthly_income", "monthly_expense_total",
        "actual_savings", "savings_rate", "credit_score", "debt_to_income_ratio",
        "income_type", "financial_scenario", "cash_flow_status",
        "financial_stress_level", "category", "savings_goal_met", "fraud_flag"
    ]
    
    st.dataframe(
        filtered_df[display_columns].sort_values("date", ascending=False),
        use_container_width=True,
        height=400
    )
    
    col1, col2 = st.columns(2)
    with col1:
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"finance_data_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.info(f"📊 Showing **{len(filtered_df):,}** records from **{filtered_df['user_id'].nunique():,}** unique users")

# ═══════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    <strong>Personal Finance Behavioral Analysis Dashboard</strong><br>
    Data Source: Kaggle Personal Finance Tracker Dataset | 3,000 records | 944 users | 2019-2023<br>
    Built with Streamlit & Plotly | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)
