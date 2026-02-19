import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Simple page config
st.set_page_config(page_title="Personal Finance Dashboard", page_icon="💰", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    return df

df = load_data()

# Header
st.title("💰 Personal Finance Behavioral Analysis Dashboard")
st.markdown("**3,000 records | 944 users | 2019-2023 | Tarmeez Capital Assessment**")
st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    years = st.multiselect("Year", sorted(df["year"].unique()), default=sorted(df["year"].unique()))
with col2:
    scenarios = st.multiselect("Scenario", sorted(df["financial_scenario"].unique()), default=sorted(df["financial_scenario"].unique()))
with col3:
    income_types = st.multiselect("Income Type", sorted(df["income_type"].unique()), default=sorted(df["income_type"].unique()))

# Filter data
fdf = df[(df["year"].isin(years)) & (df["financial_scenario"].isin(scenarios)) & (df["income_type"].isin(income_types))]

if fdf.empty:
    st.error("No data matches filters")
    st.stop()

# KPIs
st.subheader("Key Metrics")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Avg Income", f"${fdf['monthly_income'].mean():,.0f}")
k2.metric("Avg Expenses", f"${fdf['monthly_expense_total'].mean():,.0f}")
k3.metric("Avg Savings", f"${fdf['actual_savings'].mean():,.0f}")
k4.metric("Goal Met", f"{fdf['savings_goal_met'].mean()*100:.1f}%")
k5.metric("Avg Credit", f"{fdf['credit_score'].mean():.0f}")

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["Income & Expenses", "Savings Analysis", "Economic Scenarios"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Yearly Trends")
        yearly = fdf.groupby("year").agg({"monthly_income":"mean","monthly_expense_total":"mean","actual_savings":"mean"}).reset_index()
        fig = px.line(yearly, x="year", y=["monthly_income","monthly_expense_total","actual_savings"], 
                     markers=True, labels={"value":"Amount ($)", "variable":"Metric"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Income by Type")
        inc = fdf.groupby("income_type")["monthly_income"].mean().reset_index()
        fig2 = px.bar(inc, x="income_type", y="monthly_income", text_auto=".0f")
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Spending by Category")
        cat = fdf.groupby("category")["monthly_expense_total"].mean().sort_values().reset_index()
        fig3 = px.bar(cat, x="monthly_expense_total", y="category", orientation="h")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.subheader("Cash Flow Status")
        cf = fdf["cash_flow_status"].value_counts().reset_index()
        fig4 = px.pie(cf, names="cash_flow_status", values="count", hole=0.4)
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Savings Rate Distribution")
        fig5 = px.histogram(fdf, x="savings_rate", nbins=30)
        fig5.add_vline(x=fdf["savings_rate"].mean(), line_dash="dash", line_color="red")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Goal Achievement by Year")
        goal = fdf.groupby("year")["savings_goal_met"].mean().reset_index()
        goal["pct"] = goal["savings_goal_met"] * 100
        fig6 = px.bar(goal, x="year", y="pct", text_auto=".1f")
        st.plotly_chart(fig6, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Savings by Stress & Income")
        sav = fdf.groupby(["financial_stress_level","income_type"])["actual_savings"].mean().reset_index()
        fig7 = px.bar(sav, x="financial_stress_level", y="actual_savings", color="income_type", barmode="group")
        st.plotly_chart(fig7, use_container_width=True)
    
    with col4:
        st.subheader("Emergency Fund vs Savings")
        sample = fdf.sample(min(500, len(fdf)))
        fig8 = px.scatter(sample, x="emergency_fund", y="actual_savings", color="cash_flow_status", 
                         opacity=0.5, trendline="ols")
        st.plotly_chart(fig8, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metrics by Scenario")
        scen = fdf.groupby("financial_scenario").agg(
            {"monthly_income":"mean","monthly_expense_total":"mean","actual_savings":"mean"}
        ).reset_index()
        fig9 = px.bar(scen, x="financial_scenario", y=["monthly_income","monthly_expense_total","actual_savings"], barmode="group")
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        st.subheader("Stress by Scenario")
        stress = fdf.groupby(["financial_scenario","financial_stress_level"]).size().unstack(fill_value=0)
        stress_pct = stress.div(stress.sum(axis=1), axis=0) * 100
        fig10 = px.bar(stress_pct, barmode="stack")
        st.plotly_chart(fig10, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Debt-to-Income by Scenario")
        fig11 = px.box(fdf, x="financial_scenario", y="debt_to_income_ratio")
        st.plotly_chart(fig11, use_container_width=True)
    
    with col4:
        st.subheader("Investment by Scenario")
        inv = fdf.groupby(["financial_scenario","income_type"])["investment_amount"].mean().reset_index()
        fig12 = px.bar(inv, x="financial_scenario", y="investment_amount", color="income_type", barmode="group")
        st.plotly_chart(fig12, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("💡 Key Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"""
    **Savings Goal Achievement**  
    Only {fdf['savings_goal_met'].mean()*100:.1f}% of users meet their savings goals,
    despite {(fdf['cash_flow_status']=='Positive').mean()*100:.0f}% having positive cash flow.
    """)

with col2:
    recession_sav = fdf[fdf["financial_scenario"]=="recession"]["actual_savings"].mean()
    normal_sav = fdf[fdf["financial_scenario"]=="normal"]["actual_savings"].mean()
    st.warning(f"""
    **Economic Impact**  
    Recession reduces savings by ${normal_sav - recession_sav:,.0f} compared to normal periods.
    Stress levels increase significantly during downturns.
    """)

with col3:
    st.success(f"""
    **Credit Profile**  
    Average credit score: {fdf['credit_score'].mean():.0f}  
    Fraud rate: {fdf['fraud_flag'].mean()*100:.2f}%  
    Most users in Fair-Good credit range.
    """)

# Data table
with st.expander("📊 View Raw Data"):
    st.dataframe(fdf.head(100), use_container_width=True)
    st.download_button("Download CSV", fdf.to_csv(index=False), "data.csv", "text/csv")

st.caption(f"Dashboard by [Your Name] | Tarmeez Capital Assessment | {len(fdf):,} records displayed")
