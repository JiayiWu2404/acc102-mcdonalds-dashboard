import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="McDonald's Profitability Dashboard",
    layout="wide"
)

# =========================================================
# Load and prepare data
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/McDonalds_Financial_Statements.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename for consistency
    df = df.rename(columns={
        "Earnings ($B)": "Net Income ($B)"
    })

    # Sort by year ascending
    df = df.sort_values("Year").reset_index(drop=True)

    # Calculate growth rates
    df["Revenue Growth (%)"] = df["Revenue ($B)"].pct_change() * 100
    df["Net Income Growth (%)"] = df["Net Income ($B)"].pct_change() * 100

    return df


df = load_data()

# =========================================================
# Sidebar
# =========================================================
st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Revenue Trend",
        "Net Income Trend",
        "Profitability Analysis",
        "Key Insights & Limitations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

df_filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
].copy()

show_data = st.sidebar.checkbox("Show filtered data table", value=False)

# =========================================================
# Shared metrics
# =========================================================
latest_row = df_filtered.iloc[-1]
earliest_row = df_filtered.iloc[0]

highest_revenue_row = df_filtered.loc[df_filtered["Revenue ($B)"].idxmax()]
lowest_revenue_row = df_filtered.loc[df_filtered["Revenue ($B)"].idxmin()]

highest_income_row = df_filtered.loc[df_filtered["Net Income ($B)"].idxmax()]
lowest_income_row = df_filtered.loc[df_filtered["Net Income ($B)"].idxmin()]

highest_margin_row = df_filtered.loc[df_filtered["Operating Margin (%)"].idxmax()]
lowest_margin_row = df_filtered.loc[df_filtered["Operating Margin (%)"].idxmin()]

revenue_change = latest_row["Revenue ($B)"] - earliest_row["Revenue ($B)"]
income_change = latest_row["Net Income ($B)"] - earliest_row["Net Income ($B)"]
margin_change = latest_row["Operating Margin (%)"] - earliest_row["Operating Margin (%)"]

main_color = "#DB0007"
accent_color = "#FFC72C"
dark_color = "#333333"

# =========================================================
# App header
# =========================================================
st.title("McDonald's Profitability Dashboard (2002–2022)")
st.write(
    "This interactive dashboard examines how McDonald's revenue, net income, and profitability changed over time."
)
st.caption("Data source: Kaggle McDonald's Financial Statements dataset")

if show_data:
    st.subheader("Filtered Data")
    st.dataframe(df_filtered, use_container_width=True)

# =========================================================
# Page functions
# =========================================================
def render_overview(data):
    st.header("Overview")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            **Research Question**  
            Did McDonald's long-term revenue growth translate into stronger profitability from 2002 to 2022?

            **Target Users**  
            - Business students learning financial trend analysis  
            - Potential investors  
            - Industry observers interested in restaurant company performance  

            **Why this matters**  
            Revenue growth alone does not always mean better business performance.  
            This dashboard helps users evaluate whether McDonald's long-term growth was supported by stronger net income and operating margin over time.
            """
        )

    with col2:
        st.info(
            f"""
            **Selected period:** {year_range[0]} to {year_range[1]}

            **Number of years:** {len(data)}
            """
        )

    st.subheader("Key Metrics")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "Latest Revenue ($B)",
            f"{latest_row['Revenue ($B)']:.2f}"
        )

    with kpi2:
        st.metric(
            "Latest Net Income ($B)",
            f"{latest_row['Net Income ($B)']:.2f}"
        )

    with kpi3:
        st.metric(
            "Highest Revenue Year",
            f"{int(highest_revenue_row['Year'])}"
        )

    with kpi4:
        st.metric(
            "Highest Operating Margin Year",
            f"{int(highest_margin_row['Year'])}"
        )

    summary_fig = px.line(
        data,
        x="Year",
        y=["Revenue ($B)", "Net Income ($B)"],
        markers=True,
        color_discrete_sequence=[main_color, accent_color]
    )
    summary_fig.update_layout(
        title="Revenue and Net Income Over Time",
        xaxis_title="Year",
        yaxis_title="Value ($B)",
        legend_title=""
    )
    st.plotly_chart(summary_fig, use_container_width=True)

    st.markdown(
        f"""
        **Overview interpretation**  
        Within the selected period, revenue changed by **{revenue_change:.2f} billion dollars**, 
        while net income changed by **{income_change:.2f} billion dollars**.  
        This suggests that business scale and profit performance did not always move at the same pace.
        """
    )


def render_revenue_page(data):
    st.header("Revenue Trend")
    st.markdown("**Question:** How did McDonald's business scale change over time?")

    fig_revenue = px.line(
        data,
        x="Year",
        y="Revenue ($B)",
        markers=True,
        color_discrete_sequence=[main_color]
    )
    fig_revenue.update_layout(
        title="McDonald's Revenue Over Time",
        xaxis_title="Year",
        yaxis_title="Revenue ($B)"
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

    st.subheader("Revenue Growth Rate (%)")

    growth_note = st.checkbox("Show note about the first missing growth value", value=True)
    if growth_note:
        st.caption("The first year has no growth rate because there is no previous year for comparison.")

    fig_growth = px.bar(
        data,
        x="Year",
        y="Revenue Growth (%)",
        color="Revenue Growth (%)",
        color_continuous_scale="RdYlGn"
    )
    fig_growth.update_layout(
        title="Year-to-Year Revenue Growth (%)",
        xaxis_title="Year",
        yaxis_title="Revenue Growth (%)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "Highest Revenue ($B)",
            f"{highest_revenue_row['Revenue ($B)']:.2f}",
            f"Year {int(highest_revenue_row['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Revenue ($B)",
            f"{lowest_revenue_row['Revenue ($B)']:.2f}",
            f"Year {int(lowest_revenue_row['Year'])}"
        )

    st.markdown(
        f"""
        **Revenue interpretation**  
        Revenue peaked in **{int(highest_revenue_row['Year'])}** at **{highest_revenue_row['Revenue ($B)']:.2f} billion dollars**.  
        The lowest revenue in the selected period was recorded in **{int(lowest_revenue_row['Year'])}**.  
        This suggests that McDonald's business scale changed over time rather than growing at a perfectly steady pace.
        """
    )


def render_income_page(data):
    st.header("Net Income Trend")
    st.markdown("**Question:** Did profit performance move in the same way as revenue?")

    fig_income = px.line(
        data,
        x="Year",
        y="Net Income ($B)",
        markers=True,
        color_discrete_sequence=[accent_color]
    )
    fig_income.update_layout(
        title="McDonald's Net Income Over Time",
        xaxis_title="Year",
        yaxis_title="Net Income ($B)"
    )
    st.plotly_chart(fig_income, use_container_width=True)

    st.subheader("Net Income Growth Rate (%)")
    st.caption("The first year has no growth rate because year-to-year comparison starts from the second observation.")

    fig_income_growth = px.bar(
        data,
        x="Year",
        y="Net Income Growth (%)",
        color="Net Income Growth (%)",
        color_continuous_scale="RdYlGn"
    )
    fig_income_growth.update_layout(
        title="Year-to-Year Net Income Growth (%)",
        xaxis_title="Year",
        yaxis_title="Net Income Growth (%)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_income_growth, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "Highest Net Income ($B)",
            f"{highest_income_row['Net Income ($B)']:.2f}",
            f"Year {int(highest_income_row['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Net Income ($B)",
            f"{lowest_income_row['Net Income ($B)']:.2f}",
            f"Year {int(lowest_income_row['Year'])}"
        )

    st.markdown(
        f"""
        **Net income interpretation**  
        Net income reached its highest value in **{int(highest_income_row['Year'])}** and its lowest value in **{int(lowest_income_row['Year'])}**.  
        Compared with revenue, profit performance appears more volatile, which means sales growth did not always translate into equally stable profit growth.
        """
    )


def render_profitability_page(data):
    st.header("Profitability Analysis")
    st.markdown("**Question:** Was McDonald's getting better at turning sales into profit?")

    fig_margin = px.line(
        data,
        x="Year",
        y="Operating Margin (%)",
        markers=True,
        color_discrete_sequence=[dark_color]
    )
    fig_margin.update_layout(
        title="Operating Margin Over Time",
        xaxis_title="Year",
        yaxis_title="Operating Margin (%)"
    )
    st.plotly_chart(fig_margin, use_container_width=True)

    compare_fig = px.line(
        data,
        x="Year",
        y=["Revenue ($B)", "Net Income ($B)"],
        markers=True,
        color_discrete_sequence=[main_color, accent_color]
    )
    compare_fig.update_layout(
        title="Revenue vs Net Income",
        xaxis_title="Year",
        yaxis_title="Value ($B)",
        legend_title=""
    )
    st.plotly_chart(compare_fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "Highest Margin (%)",
            f"{highest_margin_row['Operating Margin (%)']:.2f}",
            f"Year {int(highest_margin_row['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Margin (%)",
            f"{lowest_margin_row['Operating Margin (%)']:.2f}",
            f"Year {int(lowest_margin_row['Year'])}"
        )
    with c3:
        st.metric(
            "Margin Change",
            f"{margin_change:.2f} pts"
        )

    st.markdown(
        f"""
        **Why margin matters**  
        Operating margin shows how efficiently the company turns revenue into operating profit.  
        In the selected period, the highest operating margin appeared in **{int(highest_margin_row['Year'])}**, while the lowest appeared in **{int(lowest_margin_row['Year'])}**.  
        This helps users see that larger sales do not automatically mean stronger profitability.
        """
    )


def render_insights_page(data):
    st.header("Key Insights & Limitations")

    st.subheader("Key Insights")

    revenue_peak_year = int(highest_revenue_row["Year"])
    income_peak_year = int(highest_income_row["Year"])
    margin_peak_year = int(highest_margin_row["Year"])

    st.markdown(
        f"""
        1. **Revenue reached its highest selected value in {revenue_peak_year},** showing that McDonald's business scale did not remain constant across the period.  
        2. **Net income peaked in {income_peak_year},** but the timing of profit strength did not necessarily match the highest revenue year.  
        3. **Operating margin was strongest in {margin_peak_year},** which suggests that profitability quality changed over time rather than moving perfectly with sales.  
        4. **Revenue changed by {revenue_change:.2f} billion dollars** across the selected years, while **net income changed by {income_change:.2f} billion dollars**, highlighting that growth and profit outcomes were not identical.  
        5. **This dashboard helps users compare business scale, profit performance, and efficiency together**, rather than relying on one metric alone.
        """
    )

    st.subheader("Limitations")
    st.markdown(
        """
        - This analysis focuses on one company only and does not compare McDonald's with competitors.
        - The dashboard depends on the accuracy and completeness of the public financial dataset.
        - External business events are not directly modeled.
        - Only selected financial indicators are included, so this is not a full valuation model.
        """
    )

    st.subheader("Future Improvements")
    st.markdown(
        """
        - Add competitor comparison, such as Starbucks or Yum! Brands  
        - Add more profitability indicators  
        - Add major event annotations on charts  
        - Add export function for filtered data  
        """
    )

    st.subheader("Why this dashboard is useful")
    st.markdown(
        """
        This dashboard is useful because it turns raw financial data into a clearer analytical story.  
        Users can see whether McDonald's growth was supported by stronger profit outcomes and operating efficiency, not just larger revenue numbers.
        """
    )


# =========================================================
# Page routing
# =========================================================
if page == "Overview":
    render_overview(df_filtered)

elif page == "Revenue Trend":
    render_revenue_page(df_filtered)

elif page == "Net Income Trend":
    render_income_page(df_filtered)

elif page == "Profitability Analysis":
    render_profitability_page(df_filtered)

elif page == "Key Insights & Limitations":
    render_insights_page(df_filtered)

# =========================================================
# Footer
# =========================================================
st.markdown("---")
st.caption(
    "Educational use only. Figures are based on the selected dataset and should be interpreted as a simplified financial analysis tool."
)