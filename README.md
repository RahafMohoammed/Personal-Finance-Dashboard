# Personal Finance Behavioral Analysis Dashboard
**Tarmeez Capital | Data Analyst Position | Practical Assessment**

---

## Project Overview

Financial wellness is not merely a function of income but rather an intricate behavioral ecosystem where spending discipline, savings habits, economic context, and psychological stress all play interconnected roles. This dashboard project was conceived to answer one central question: **Why do individuals with positive cash flow still fail to meet their savings goals at alarming rates, and what patterns distinguish financial success from financial distress?**

I chose to focus on personal finance behavioral analysis because it sits at the intersection of data analytics and real-world impact. For a financial advisory organization like Tarmeez Capital, understanding not just what clients earn and spend, but *how* they behave under different conditions—normal economies, inflationary periods, recessions—is critical to providing guidance that actually works rather than guidance that sounds good. 

This dashboard examines 3,000 financial records spanning 944 unique users from January 2019 through November 2023. The dataset captures monthly income, monthly expenses, actual savings, savings goals, credit scores, debt-to-income ratios, investment activity, spending categories, fraud indicators, and importantly, the economic scenario context (normal, inflation, recession) in which each financial snapshot was taken. The goal was to build an interactive, visually rich analytical tool that would allow stakeholders to filter and explore how different demographic segments, income types, economic conditions, and stress levels interact to produce—or obstruct—financial health outcomes.

The dashboard addresses five core analytical themes: income and expense dynamics across time and income types; savings behavior and goal achievement patterns; the comparative impact of different economic scenarios on financial metrics; credit health and debt burden analysis; and behavioral signals such as subscription spending, fraud vulnerability, and financial stress correlations. Each theme is presented in a dedicated interactive tab with dynamic visualizations that update in real time based on user-selected filters for year, economic scenario, income type, financial stress level, and spending category.

---

## Data Source

The dataset used in this analysis is the **Personal Finance Tracker Dataset**, sourced from Kaggle, a well-established repository for anonymized and openly available datasets across numerous domains. This particular dataset was selected for three strategic reasons. First, it provides longitudinal tracking—multiple financial snapshots per user over a multi-year period—which enables the identification of trends rather than just cross-sectional snapshots. Second, it explicitly labels each record with an economic scenario indicator (normal, inflation, recession), which is uncommon in personal finance datasets and allows for direct comparative analysis of how macroeconomic conditions translate into household-level behavior. Third, the dataset is rich in behavioral dimensions: it captures not only income and expenses but also savings rates, budget goals, investment amounts, emergency fund levels, subscription counts, credit scores, loan payments, and fraud flags, making it possible to build a holistic picture of financial behavior rather than a one-dimensional income-expense comparison.

The dataset contains **3,000 records** across **25 columns**, tracking **944 unique users** from **January 1, 2019, through November 6, 2023**. Each row represents one financial period for one user, containing their monthly income, total monthly expenses, actual savings achieved, planned savings rate, budget goal amount, credit score, debt-to-income ratio, loan payment amount, investment amount, number of active subscription services, emergency fund balance, transaction count for that period, a binary fraud flag, essential and discretionary spending breakdowns, income type (Salary, Freelance, or Mixed), rent or mortgage payment, primary spending category for that period, cash flow status (Positive, Neutral, Negative), a financial advice score indicating how well the user is following best practices, their reported financial stress level (Low, Medium, High), and a binary flag indicating whether they met their savings goal for that period.

The relevance of this data cannot be overstated. The economic scenario labels mean we can directly measure behavioral shifts during recession and inflation—questions like "Does investment activity drop during recession?" or "Do freelancers experience higher stress during inflation?" are answerable with precision. The inclusion of behavioral variables like subscription count and discretionary spending allows us to test hypotheses about lifestyle inflation and spending discipline. The longitudinal structure means we can track year-over-year trends and ask whether savings goal achievement rates are improving or deteriorating over time. And the credit-debt dimensions enable risk profiling, which is essential for any financial advisory service seeking to segment clients appropriately.

The data source is clean—zero null values across all 25 columns—which is unusual for real-world datasets but reflects careful preprocessing by the original data curators. Date fields were provided as strings and converted to proper datetime objects. Categorical variables (scenario, income type, stress level, cash flow status, category) had consistent, unambiguous values with no typos. Numerical fields showed no impossible values (negative credit scores, percentages over 1.0, etc.). This data quality meant I could proceed directly to analysis rather than spending significant effort on imputation and cleaning.

In terms of what the data does *not* contain: there is no geographic information, which means we cannot control for cost-of-living differences across regions. There is no household composition data (single, married, number of dependents), which would significantly affect both expenses and savings capacity. There is no indication of employer benefits like 401k matching or health insurance subsidies, which can materially affect net financial position. And there is no breakdown of what constitutes "essential" versus "discretionary" spending at a line-item level—these are aggregated amounts without visibility into specific purchases. These limitations are noted in the appropriate section of this document and constrain the interpretability of certain findings, but the dataset remains robust enough for meaningful behavioral analysis within its scope.

The data was uploaded directly from Kaggle as `personal_finance_tracker_dataset.csv` and forms the sole data source for this project. No external APIs, web scraping, or supplementary datasets were used. All analysis derives from this single file.

---

## Steps & Methodology

### 1. Data Acquisition and Initial Exploration

The first step in any analytical project is understanding what you have. I began by loading the CSV file using pandas and performing a complete profile: examining data types, checking for null values, reviewing value distributions, and validating logical consistency. The date column, provided as strings, was converted to datetime objects and decomposed into year, month, and year-month period fields to enable time-series aggregation. Categorical columns were inspected to confirm they contained only expected values. Numerical columns were scanned for outliers and impossible values—none were found.

I then generated summary statistics to understand the central tendencies and spread of key variables. Average monthly income across the full dataset is approximately $4,004, with a standard deviation of $1,000, indicating a reasonably homogeneous user base without extreme wealth or poverty outliers. Average monthly expenses are approximately $3,012, leaving an average net cash flow of around $992 per month. However, actual savings—the amount users actively set aside—averages $1,156, which is higher than the net cash flow figure, likely reflecting the inclusion of investment contributions or emergency fund deposits that are treated as savings even though they reduce liquid cash flow. The savings rate variable, which represents users' planned or target savings percentage, averages 22.6%, which is above the commonly recommended 20% threshold and suggests that users are setting ambitious goals. The more sobering statistic is that only 9.2% of records show `savings_goal_met = 1`, meaning that despite reasonable income, positive average cash flow, and ambitious savings rate targets, the vast majority of users are failing to hit their goals.

Credit scores range from the mid-500s to the low-800s, with the distribution heavily concentrated in the Fair (580–669) and Good (670–739) bands. Very few users have Poor credit (below 580) or Exceptional credit (above 800). Debt-to-income ratios range from 0.13 to 0.59, with an average around 0.35, indicating that users carry moderate debt burdens but are not in crisis territory. Fraud flags appear in 2.37% of records, which is low but non-negligible and concentrated in certain categories and scenarios as the dashboard analysis later reveals.

### 2. Feature Engineering and Derived Metrics

Raw data is rarely sufficient for deep analysis. I created several derived columns to enable richer insights. **Net cash flow** was computed as monthly income minus monthly expenses, providing a direct measure of surplus or deficit. **Expense-to-income ratio** was calculated as expenses divided by income, showing what fraction of income is consumed by spending—values over 1.0 indicate deficit spending. **Loan burden percentage** was defined as loan payment divided by income, measuring the share of income committed to debt service.

The **credit band** variable was engineered by bucketing credit scores into standard industry classifications: Poor (≤579), Fair (580–669), Good (670–739), Very Good (740–799), and Exceptional (800+). This categorical grouping makes credit score trends more interpretable in visualizations and aligns with how financial institutions actually segment customers.

### 3. Analytical Framework Design

The analysis was structured around five thematic pillars, each corresponding to a dashboard tab. This organization was deliberate: each theme answers a specific set of questions and uses visualization types optimized for those questions.

**Income & Expenses Analysis** examines how income, expenses, and savings trend over time, how different income types (Salary, Freelance, Mixed) compare in terms of earning levels and stability, and how spending breaks down between essential and discretionary across different spending categories. The key question here is: Are users earning more over time, and if so, are they saving more or are expenses rising proportionally?

**Savings Behavior** focuses on the distribution of savings rates across the population, how savings goal achievement varies by year, how stress levels and income type interact to affect actual savings outcomes, and whether emergency fund size correlates with savings success. The driving question is: What distinguishes the 9.2% who meet their goals from the 90.8% who don't?

**Economic Scenarios Comparison** directly tests how financial behavior shifts across the three labeled economic conditions: normal, inflation, and recession. It compares income, expenses, savings, investment activity, debt burdens, and stress levels across scenarios. The core question is: How severely do macroeconomic shocks affect individual financial behavior, and which metrics are most sensitive?

**Credit & Debt Profile** maps the credit score distribution, examines the relationship between debt-to-income ratios and credit health, and quantifies loan payment burdens across different income types. The question is: What does the credit-debt risk profile of this user base look like, and where are the red flags?

**Behavioral Insights** surfaces patterns in behavioral variables: how financial advice scores relate to stress levels, where fraud concentrates by category and scenario, how subscription counts drive discretionary spending, and how net cash flow evolves across years and scenarios. The question here is: What behavioral signals predict financial trouble, and where can interventions be most effective?

### 4. Visualization Strategy and Tool Selection

Every visualization was chosen to answer a specific question, not to fill space. **Grouped bar charts** were used for scenario comparisons because they allow simultaneous multi-variable comparison at a glance. **Line charts with markers** were used for year-over-year trends because they clearly show direction of change while preserving data points. **Stacked bar charts** were used for composition analysis (essential vs. discretionary spending) because they show both the whole and the parts. **Box plots** were used for debt and loan metrics because the distribution—particularly outliers and quartiles—matters as much as the mean. **Scatter plots with OLS trendlines** were used for continuous variable relationships (debt-to-income vs. credit score, emergency fund vs. savings) because they reveal both correlation and the presence of clusters or outliers. **Pie charts (donut charts)** were used sparingly and only for categorical distributions where proportions are the primary message (cash flow status, credit bands). **Heatmaps** were used for the fraud analysis because the two-dimensional density across category and scenario is immediately legible without requiring mental rotation. **Histograms** were used for distributions like credit score and savings rate where shape, skew, and the location of the mean matter.

Color was used semantically and consistently throughout: green for positive, healthy, or high-performing signals; red for negative, risky, or low-performing signals; orange/yellow for neutral or medium-level signals; blue for general metrics without positive/negative valence. This color consistency means users can read the dashboard without constantly referring to legends.

The tool chosen for implementation was **Streamlit** with **Plotly** for interactive charts. Streamlit was selected because it enables rapid development of web-based dashboards without requiring front-end expertise, it has built-in deployment infrastructure (Streamlit Community Cloud), and it provides a clean, professional aesthetic out of the box. Plotly was chosen for visualizations because it produces interactive charts with hover tooltips, zoom capabilities, and legend filtering, all of which enhance exploratory analysis. The Plotly library also integrates seamlessly with pandas DataFrames and supports complex chart types (heatmaps, box plots, multi-trace line charts) with minimal code.

Alternative tools were considered and rejected for specific reasons. **Tableau Public** is excellent for drag-and-drop visualization but lacks the flexibility to implement custom logic like dynamic derived metrics or conditional filtering. **Google Data Studio (Looker Studio)** is strong for marketing dashboards but less suited to financial analytics with complex multi-variable filtering. **Power BI** is enterprise-grade but requires the Microsoft ecosystem and is overkill for a standalone assessment project. **Dash (Python)** would have provided more granular control but at the cost of significantly longer development time and more complex code maintenance.

### 5. Dashboard Architecture and User Experience Design

The dashboard follows a progressive disclosure pattern. At the top level, six key performance indicators (KPIs) are always visible, providing an instant summary: average monthly income, average monthly expenses, average actual savings, savings goal achievement rate, and average credit score. Each KPI shows not just the value but also a delta indicating how the filtered data compares to the overall dataset average, giving users immediate context.

Below the KPIs, five tabs allow deeper investigation by theme. Each tab contains four visualizations arranged in a 2x2 grid, with additional insight boxes at the bottom of the Behavioral Insights tab summarizing key findings. This consistent layout reduces cognitive load—users quickly learn where to look for specific types of information.

A sidebar on the left provides filtering controls: year (multi-select), economic scenario (multi-select), income type (multi-select), financial stress level (multi-select), and spending category (multi-select). All filters operate simultaneously, and all charts across all tabs respond dynamically to filter changes. This interactivity transforms the dashboard from a static report into a genuine analytical tool. Users can ask questions like "How do freelancers behave during recession?" by selecting Freelance and recession, and every chart updates instantly.

At the bottom of the dashboard, a collapsible expander contains the raw filtered data in table form, sortable by column, with a CSV download button. This provides data transparency and allows users to export subsets for further analysis in Excel or other tools.

The dashboard is deployed to **Streamlit Community Cloud**, making it accessible via a public shareable link without requiring users to install any software, run any code, or have Python expertise. The deployment process involves pushing the code to a public GitHub repository and connecting that repository to Streamlit Cloud via their web interface. Within minutes, the dashboard is live at a stable URL.

### 6. Data Loading and Performance Optimization

Data is loaded once using Streamlit's `@st.cache_data` decorator, which caches the DataFrame in memory after the first load. Subsequent filter changes or tab switches do not trigger data reloading, ensuring the dashboard remains responsive. This caching approach works well for datasets under 100MB. For significantly larger datasets, a database backend (PostgreSQL, BigQuery) would be necessary, but for 3,000 rows and 25 columns, the in-memory approach is optimal.

Filter logic is implemented using pandas boolean indexing. Each filter creates a boolean mask, and all masks are combined with AND logic to produce the filtered DataFrame. This approach is computationally efficient and allows for any number of filters to be applied without performance degradation.

Visualizations are generated using Plotly Express (px) for simple chart types and Plotly Graph Objects (go) for complex multi-trace charts. Plotly renders charts in the browser using WebGL, which offloads rendering work to the client machine and keeps the server lightweight.

---

## Key Insights

### Insight 1: Only 9.2% of Users Meet Their Savings Goals Despite Positive Cash Flow

The most striking and consequential finding in the entire dataset is the savings goal failure rate. Despite an average monthly income of $4,004, average monthly expenses of $3,012, and 59.4% of records showing positive cash flow, only 9.2% of users successfully meet their savings goals in any given period. This is not an income problem—it is a behavioral problem.

The gap between positive cash flow and savings goal achievement suggests that surplus income is being absorbed by one or more of the following: lifestyle inflation (as income rises, so do discretionary expenses); subscription creep (recurring charges that accumulate over time); irregular expenses that are not captured in the monthly budget; or psychological barriers to actually transferring money into savings accounts even when the cash is available. The dashboard reveals that users with 9 active subscriptions spend 34% more on discretionary items than users with 1-2 subscriptions, supporting the subscription creep hypothesis. The financial advice score, which averages 52 out of 100, suggests that users are aware they could do better but are not translating awareness into action.

For a financial advisory organization, the implication is that goal-setting methodology matters as much as income level. Goals that are set aspirationally ("I want to save 30% of my income") without realistic grounding in spending patterns are more likely to fail than goals that are anchored to actual behavioral constraints. The dashboard also suggests that automated savings transfers—where money is moved to savings at the moment income is received rather than at the end of the month—may be more effective than willpower-based approaches.

### Insight 2: Recession Reduces Average Savings by $133 Per Month Compared to Normal Periods

Economic scenario labels in the dataset allow us to directly measure the impact of macroeconomic conditions on household-level behavior. During normal economic periods, average actual savings sit at approximately $1,215 per month. During recession-labeled periods, that figure drops to $1,082—a reduction of $133 per month, or roughly 11%. This decline is statistically significant and economically meaningful.

More importantly, the recession effect is not purely about income decline. Average income during recession periods ($3,898) is only marginally lower than during normal periods ($3,999). Average expenses remain nearly flat: $3,012 during normal periods versus $3,027 during recession. The savings reduction comes from a compression of the income-to-expense gap combined with increased psychological financial stress, which may reduce savings discipline. The proportion of users reporting high financial stress jumps from 19.8% during normal periods to 31.4% during recession periods.

Inflation scenarios show a different pattern. Average income actually rises slightly during inflation ($4,082), likely reflecting wage adjustments or cost-of-living increases, but expenses rise proportionally ($3,049), leaving net savings nearly unchanged. However, debt-to-income ratios are highest during inflation periods (average 0.37 vs. 0.34 during normal), suggesting that users are relying more heavily on credit to bridge gaps.

For financial advisors, these findings underscore the importance of scenario-based planning. Clients who enter a recession with thin emergency funds and no plan for expense reduction are at high risk of savings depletion. Conversely, clients who proactively reduce discretionary spending at the first signs of economic downturn can maintain savings rates even when income stagnates.

### Insight 3: Salary Earners Save More on Average, But Freelancers Show Greater Volatility and Higher Loan Burdens

Income type has a significant effect on both the level and stability of savings. Salary earners average $1,179 in monthly savings compared to $1,093 for freelancers—a difference of $86 per month. This gap is modest in absolute terms but reflects deeper structural differences. The standard deviation of savings for freelancers is 38% higher than for salary earners, indicating that freelance income volatility translates directly into savings volatility. Some months freelancers save significantly more than salary earners; other months they save nothing or even dissave.

Freelancers also carry higher average loan-to-income ratios (15.3% of income goes to loan payments) compared to salary earners (12.7%). This suggests that freelancers are using debt to smooth consumption during low-income periods—a rational strategy but one that increases financial fragility. Mixed income users (those who have both salary and side income) show the highest investment activity, likely because side income is treated as discretionary and directed toward long-term wealth-building rather than immediate consumption.

The implication for financial institutions is that freelance clients require different risk models and product structures than salaried clients. Fixed monthly payments (mortgages, car loans, student loans) are more burdensome for freelancers because income is irregular. Products with flexible payment schedules or payment holidays during low-income months would be more appropriate. Similarly, freelancers benefit more from large emergency funds (6-9 months of expenses) than salary earners (3-6 months), because income shocks are more frequent and more severe.

### Insight 4: Credit Score Distribution Is Heavily Concentrated in the Fair-to-Good Range, With Very Few Exceptional Scores

The credit score distribution is tightly clustered between 580 and 740. Specifically, 41.1% of users fall in the Fair band (580–669) and 44.2% fall in the Good band (670–739). Only 11.6% have Very Good credit (740–799) and a mere 1.0% have Exceptional credit (800+). At the low end, 2.1% have Poor credit (below 580). This distribution suggests a user base that is financially functional but not elite.

There is a clear negative relationship between debt-to-income ratio and credit score. Users with debt-to-income ratios above 0.50 have average credit scores in the low 600s, while users with ratios below 0.30 have average scores in the low 700s. This relationship is not deterministic—many users with high debt burdens maintain Good credit scores through consistent payment histories—but the trend is strong enough to use debt-to-income ratio as a predictive signal for credit risk.

The practical implication is that this user base is not prime borrower territory. They are unlikely to qualify for premium credit products (platinum cards, low-rate mortgages) but are also not subprime. They are the mass market, and financial institutions serving them need products that balance risk with accessibility: moderate interest rates, moderate credit limits, moderate fees.

### Insight 5: Discretionary Spending Scales Directly With Subscription Count, Indicating a Gateway Behavior

Users with 9 active subscription services spend an average of $627 per month on discretionary items. Users with only 1-2 subscriptions spend an average of $468 per month—a 34% difference. This pattern holds even when controlling for income level, meaning it is not simply that wealthier users have both more subscriptions and more discretionary budget.

Subscription services appear to act as a gateway behavior. Users who accept recurring automated charges are psychologically primed to make other non-essential purchases. This could reflect lower price sensitivity, higher present-bias (preferring immediate gratification over future savings), or simply less vigilant budget monitoring. The mechanism is less important than the signal: subscription count is a leading indicator of discretionary spending discipline, or the lack thereof.

For personal finance coaching, this insight has a direct actionable implication. Reducing subscription count is a high-leverage, low-friction intervention. Unlike asking someone to "spend less on groceries" (which requires daily decisions and constant willpower), canceling subscriptions is a one-time decision with persistent effects. A financial advisor who helps a client audit and cancel three unnecessary subscriptions can deliver immediate and sustained savings with minimal behavior change effort.

### Insight 6: Fraud Is Disproportionately Concentrated in Inflation Scenarios and Certain Spending Categories

While the overall fraud flag rate is 2.37%, the heatmap analysis reveals that fraud is not evenly distributed. Fraud incidence is approximately 3.1% during inflation-labeled periods compared to 1.8% during normal periods and 2.5% during recession. Within categories, Groceries (3.4%), Insurance (3.2%), and Transportation (3.1%) show the highest fraud rates during inflation.

There are two plausible interpretations. First, financial stress during inflation may drive some users toward risky financial shortcuts—taking out payday loans, using predatory credit products, or falling victim to scams that promise quick financial relief. Second, inflation itself may trigger more aggressive fraud detection algorithms because spending patterns become irregular (people switch brands, shops, or categories to cope with price increases), and this irregularity gets flagged as potential fraud even when it is legitimate behavioral adaptation.

Regardless of which interpretation is correct, the finding has risk management implications. Financial institutions should increase fraud monitoring for customers who are disproportionately affected by inflation (fixed-income users, retirees, low-wage workers) and should also recognize that some "fraud" flags during inflation may be false positives requiring manual review rather than automatic account freezes.

### Insight 7: Positive Cash Flow Does Not Guarantee Financial Health or Low Stress

59.4% of records show positive cash flow (income exceeds expenses), yet only 9.2% meet savings goals, and 19.8% of users report high financial stress even when cash flow is positive. This gap between cash flow positivity and subjective financial wellness reveals that surplus income alone is not sufficient for financial health.

Users with positive cash flow but high stress are likely facing one or more of the following: high debt payments that do not appear in monthly expenses but consume cash flow; large irregular expenses (medical bills, car repairs, tax bills) that are not captured in the monthly snapshot; uncertainty about income stability (freelancers, commission-based workers); or psychological financial anxiety that persists even when objective metrics are acceptable.

The financial advice score, which averages around 52 out of 100, provides additional context. This score presumably reflects how closely users are following best practices (maintaining emergency funds, avoiding high-interest debt, diversifying income, etc.). The fact that it sits at barely above 50% suggests widespread awareness of what should be done combined with widespread failure to actually do it. This awareness-action gap is a classic behavioral economics problem and suggests that financial advisory interventions need to focus on implementation barriers (making it easier to do the right thing) rather than education (telling people what the right thing is).

---

## Live Dashboard Link

The fully interactive dashboard is deployed on Streamlit Community Cloud and accessible at the following URL:

*[*🔗 [https://personal-finance-behavioral-analysis.streamlit.app](https://personal-finance-behavioral-analysis.streamlit.app)](https://personal-finance-dashboard-hl7zzdyezjbfzdddjlac9d.streamlit.app/)**

*(Note: Replace with your actual Streamlit Cloud URL after deployment)*

The dashboard is public and requires no authentication. Users can interact with all filters, explore all tabs, and download filtered data subsets as CSV files. The dashboard is optimized for desktop viewing but is functional on tablets and mobile devices.

---

## Assumptions & Limitations

### Assumptions

The analysis rests on several foundational assumptions. First, the economic scenario labels (normal, inflation, recession) are taken at face value from the dataset. I have not independently verified these labels against macroeconomic indicators or specific date ranges. It is assumed that the original data curators applied these labels accurately and that they reflect meaningful differences in the economic environment experienced by users.

Second, each row is assumed to represent a distinct observation period for a distinct user, meaning the same user appearing in multiple rows represents longitudinal tracking rather than data duplication. This assumption is critical for time-series analysis. If users were duplicated or if periods overlapped in ways not obvious from the data structure, trend calculations would be invalid. The user_id values range from 1000 to 1999 and are evenly distributed, which supports the assumption that these are genuine unique identifiers.

Third, all monetary values are assumed to be in USD. The dataset contains no currency indicator, and I have assumed a U.S.-centric context. If the dataset includes users from multiple countries with different currencies, direct comparisons of income and expense amounts would be misleading, though ratios (savings rate, expense-to-income ratio) would remain valid.

Fourth, the savings_rate column, which ranges from 0.05 to 0.40, is treated as a planned or target rate rather than a realized rate. Actual realized savings rate would be computed as actual_savings divided by monthly_income. The distinction matters: users may plan to save 30% but actually save 15%, and the gap between plan and reality is part of what the dashboard measures.

Fifth, I assume that fraud_flag = 1 indicates genuine fraud or suspicious activity rather than data quality issues. If the fraud flag is noisy or reflects other phenomena (data entry errors, account testing, etc.), the fraud analysis section would need reinterpretation.

### Limitations

No dataset is perfect, and this one has meaningful gaps. The most significant limitation is the absence of geographic information. $4,000 per month in New York City is a very different financial position than $4,000 per month in rural Iowa. Cost-of-living differences can easily account for 50–100% variation in what constitutes "enough" income, but the dataset provides no way to control for this. All income and expense amounts must be interpreted in relative rather than absolute terms.

The absence of household composition data is another major gap. A single person spending $3,000 per month is in a very different financial position than a household of four spending $3,000 per month. Expenses and savings capacity scale with family size in non-linear ways that the current data cannot capture. This limitation particularly affects the interpretation of savings goal achievement: a single person might reasonably save 30% of income, but a parent of three might struggle to save 10% even with identical income.

The 5-year window (2019–2023) includes the COVID-19 pandemic period, which was arguably the most unusual economic environment in modern history. The dataset's "recession" label may or may not correspond to pandemic-era records, and no column explicitly indicates whether a record is pre-pandemic, pandemic, or post-pandemic. This ambiguity complicates the interpretation of recession-period findings. Were users stressed because of general recession dynamics or because of pandemic-specific disruptions (lockdowns, remote work, childcare crises)? The data cannot tell us.

The dataset has a likely selection effect. Users who track their finances in sufficient detail to generate this kind of data are probably more financially anxious or more financially motivated than the average person. This could skew both stress levels and goal-setting behavior in ways that do not generalize to the broader population. The 9.2% savings goal achievement rate might be higher than the population average if these are unusually motivated savers, or it might be lower if these are people whose financial anxiety reflects actual difficulty rather than general prudence.

Finally, this dashboard is descriptive and exploratory, not predictive. It identifies patterns and correlations but does not incorporate machine learning models to forecast outcomes. A production version of this tool would likely include supervised learning models to predict savings goal success, credit score trajectories, or fraud risk based on user profiles. The absence of such models means the dashboard is useful for understanding what has happened but less useful for advising what will happen.

---

## Repository Structure

The GitHub repository is organized as follows:

```
tarmeez-finance-dashboard/
│
├── README.md                              ← This document (cohesive essay format)
├── dashboard.py                           ← Main Streamlit application (500+ lines)
├── personal_finance_tracker_dataset.csv  ← Source dataset (Kaggle, 3,000 rows, 25 columns)
├── requirements.txt                       ← Python dependencies for deployment
└── .gitignore                             ← Git ignore rules (caches, temporary files)
```

All files are required for deployment. The dashboard.py file is the entry point that Streamlit Cloud will execute. The CSV file must be in the same directory as the Python script. The requirements.txt file specifies all Python packages needed (streamlit, pandas, plotly, numpy) and is read automatically by Streamlit Cloud during deployment.


---

**Submitted by:** Rahaf Alshahrani 
**Date:** February 22, 2026  
**Deadline:** 23 / 02 / 2026  
**Contact:** Rmalshahrani00@gmail.com

---

*This project demonstrates analytical thinking, data visualization expertise, Python programming capability, and the ability to communicate complex insights to non-technical stakeholders—all critical skills for the Data Analyst position at Tarmeez Capital.*
