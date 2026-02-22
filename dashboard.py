import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Personal Finance Dashboard", page_icon="💰", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("personal_finance_tracker_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    return df

df = load_data()

st.title("💰 Personal Finance Behavioral Analysis Dashboard")
st.markdown("**3,000 records | 944 users | 2019-2023 | Tarmeez Capital Assessment**")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    years = st.multiselect("Year", sorted(df["year"].unique()), default=sorted(df["year"].unique()))
with col2:
    scenarios = st.multiselect("Scenario", sorted(df["financial_scenario"].unique()), default=sorted(df["financial_scenario"].unique()))
with col3:
    income_types = st.multiselect("Income Type", sorted(df["income_type"].unique()), default=sorted(df["income_type"].unique()))

fdf = df[(df["year"].isin(years)) & (df["financial_scenario"].isin(scenarios)) & (df["income_type"].isin(income_types))]

if fdf.empty:
    st.error("No data matches filters")
    st.stop()

st.subheader("Key Metrics")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Avg Income", f"${fdf['monthly_income'].mean():,.0f}")
k2.metric("Avg Expenses", f"${fdf['monthly_expense_total'].mean():,.0f}")
k3.metric("Avg Savings", f"${fdf['actual_savings'].mean():,.0f}")
k4.metric("Goal Met", f"{fdf['savings_goal_met'].mean()*100:.1f}%")
k5.metric("Avg Credit", f"{fdf['credit_score'].mean():.0f}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📈 Income & Expenses", "💰 Savings Analysis", "🌐 Economic Scenarios"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Yearly Trends")
        yearly = fdf.groupby("year").agg({"monthly_income":"mean","monthly_expense_total":"mean","actual_savings":"mean"}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly["year"], y=yearly["monthly_income"], mode='lines+markers', name='Income', line=dict(color='#2ecc71', width=3)))
        fig.add_trace(go.Scatter(x=yearly["year"], y=yearly["monthly_expense_total"], mode='lines+markers', name='Expenses', line=dict(color='#e74c3c', width=3)))
        fig.add_trace(go.Scatter(x=yearly["year"], y=yearly["actual_savings"], mode='lines+markers', name='Savings', line=dict(color='#3498db', width=3)))
        fig.update_layout(height=400, xaxis_title="Year", yaxis_title="Amount ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Income by Type")
        inc = fdf.groupby("income_type")["monthly_income"].mean().reset_index()
        fig2 = px.bar(inc, x="income_type", y="monthly_income", text=inc["monthly_income"].apply(lambda x: f"${x:,.0f}"))
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Spending by Category")
        cat = fdf.groupby("category")["monthly_expense_total"].mean().sort_values().reset_index()
        fig3 = px.bar(cat, x="monthly_expense_total", y="category", orientation="h")
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.subheader("Cash Flow Status")
        cf = fdf["cash_flow_status"].value_counts().reset_index()
        cf.columns = ["Status", "Count"]
        colors = {"Positive": "#2ecc71", "Neutral": "#f39c12", "Negative": "#e74c3c"}
        fig4 = px.pie(cf, names="Status", values="Count", hole=0.4, color="Status", color_discrete_map=colors)
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Savings Rate Distribution")
        fig5 = px.histogram(fdf, x="savings_rate", nbins=30, color_discrete_sequence=['#3498db'])
        fig5.add_vline(x=fdf["savings_rate"].mean(), line_dash="dash", line_color="red", annotation_text=f"Mean: {fdf['savings_rate'].mean():.2f}")
        fig5.update_layout(height=350, xaxis_title="Savings Rate", yaxis_title="Count")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Goal Achievement by Year")
        goal = fdf.groupby("year")["savings_goal_met"].mean().reset_index()
        goal["pct"] = goal["savings_goal_met"] * 100
        fig6 = px.bar(goal, x="year", y="pct", text=goal["pct"].apply(lambda x: f"{x:.1f}%"), color="pct", color_continuous_scale="RdYlGn")
        fig6.update_traces(textposition="outside")
        fig6.update_layout(height=350, showlegend=False, yaxis_title="Goal Met (%)")
        st.plotly_chart(fig6, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Savings by Stress & Income")
        sav = fdf.groupby(["financial_stress_level","income_type"])["actual_savings"].mean().reset_index()
        fig7 = px.bar(sav, x="financial_stress_level", y="actual_savings", color="income_type", barmode="group", category_orders={"financial_stress_level": ["Low", "Medium", "High"]})
        fig7.update_layout(height=350, yaxis_title="Avg Savings ($)")
        st.plotly_chart(fig7, use_container_width=True)
    
    with col4:
        st.subheader("Emergency Fund vs Savings")
        sample = fdf.sample(min(500, len(fdf)), random_state=42)
        colors_map = {"Positive": "#2ecc71", "Neutral": "#f39c12", "Negative": "#e74c3c"}
        fig8 = px.scatter(sample, x="emergency_fund", y="actual_savings", color="cash_flow_status", opacity=0.6, color_discrete_map=colors_map)
        fig8.update_layout(height=350, xaxis_title="Emergency Fund ($)", yaxis_title="Actual Savings ($)")
        st.plotly_chart(fig8, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metrics by Scenario")
        scen = fdf.groupby("financial_scenario").agg({"monthly_income":"mean","monthly_expense_total":"mean","actual_savings":"mean"}).reset_index()
        fig9 = go.Figure()
        fig9.add_trace(go.Bar(x=scen["financial_scenario"], y=scen["monthly_income"], name="Income", marker_color='#2ecc71'))
        fig9.add_trace(go.Bar(x=scen["financial_scenario"], y=scen["monthly_expense_total"], name="Expenses", marker_color='#e74c3c'))
        fig9.add_trace(go.Bar(x=scen["financial_scenario"], y=scen["actual_savings"], name="Savings", marker_color='#3498db'))
        fig9.update_layout(barmode="group", height=370, yaxis_title="Amount ($)")
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        st.subheader("Stress by Scenario")
        stress = fdf.groupby(["financial_scenario","financial_stress_level"]).size().unstack(fill_value=0)
        stress_pct = stress.div(stress.sum(axis=1), axis=0) * 100
        fig10 = go.Figure()
        stress_colors = {"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"}
        for stress_level in ["Low", "Medium", "High"]:
            if stress_level in stress_pct.columns:
                fig10.add_trace(go.Bar(x=stress_pct.index, y=stress_pct[stress_level], name=stress_level, marker_color=stress_colors[stress_level]))
        fig10.update_layout(barmode="stack", height=370, yaxis_title="Percentage (%)")
        st.plotly_chart(fig10, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Debt-to-Income by Scenario")
        fig11 = px.box(fdf, x="financial_scenario", y="debt_to_income_ratio", color="financial_scenario")
        fig11.update_layout(height=340, showlegend=False, yaxis_title="Debt-to-Income Ratio")
        st.plotly_chart(fig11, use_container_width=True)
    
    with col4:
        st.subheader("Investment by Scenario")
        inv = fdf.groupby(["financial_scenario","income_type"])["investment_amount"].mean().reset_index()
        fig12 = px.bar(inv, x="financial_scenario", y="investment_amount", color="income_type", barmode="group")
        fig12.update_layout(height=340, yaxis_title="Avg Investment ($)")
        st.plotly_chart(fig12, use_container_width=True)

st.markdown("---")
st.subheader("💡 Key Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"""**Savings Goal Achievement**  
Only {fdf['savings_goal_met'].mean()*100:.1f}% meet their goals, despite {(fdf['cash_flow_status']=='Positive').mean()*100:.0f}% having positive cash flow.""")

with col2:
    if "recession" in fdf["financial_scenario"].values and "normal" in fdf["financial_scenario"].values:
        rec_sav = fdf[fdf["financial_scenario"]=="recession"]["actual_savings"].mean()
        nor_sav = fdf[fdf["financial_scenario"]=="normal"]["actual_savings"].mean()
        st.warning(f"""**Economic Impact**  
Recession reduces savings by ${nor_sav - rec_sav:,.0f} vs normal periods.""")
    else:
        st.warning("**Economic Impact** - Select multiple scenarios to compare")

with col3:
    st.success(f"""**Credit Profile**  
Avg score: {fdf['credit_score'].mean():.0f}  
Fraud rate: {fdf['fraud_flag'].mean()*100:.2f}%""")

with st.expander("📊 View Raw Data"):
    st.dataframe(fdf.head(100), use_container_width=True)
    st.download_button("Download CSV", fdf.to_csv(index=False).encode('utf-8'), "data.csv", "text/csv")

st.caption(f"Personal Finance Dashboard | Tarmeez Capital | {len(fdf):,} records | Built by Rahaf Mohammed")
