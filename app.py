import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

    # Calculate growth rates on full dataset
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
        "Full Data Overview",
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

# Recalculate growth rates within the filtered data
df_filtered["Revenue Growth (%)"] = df_filtered["Revenue ($B)"].pct_change() * 100
df_filtered["Net Income Growth (%)"] = df_filtered["Net Income ($B)"].pct_change() * 100

show_data = st.sidebar.checkbox("Show filtered data table", value=False)
show_explanations = st.sidebar.checkbox("Show chart explanations", value=True)

# =========================================================
# Colors and style
# =========================================================
main_color = "#DB0007"
accent_color = "#FFC72C"
dark_color = "#333333"
soft_gray = "#F5F5F5"

PLOT_TEMPLATE = "plotly_white"

# =========================================================
# Helper functions
# =========================================================
def fmt_billions(value):
    return f"{value:.2f}"

def fmt_percent(value):
    return f"{value:.2f}%"

def to_csv_download(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

def get_metrics(data):
    if data.empty:
        return None

    latest_row = data.iloc[-1]
    earliest_row = data.iloc[0]

    highest_revenue_row = data.loc[data["Revenue ($B)"].idxmax()]
    lowest_revenue_row = data.loc[data["Revenue ($B)"].idxmin()]

    highest_income_row = data.loc[data["Net Income ($B)"].idxmax()]
    lowest_income_row = data.loc[data["Net Income ($B)"].idxmin()]

    highest_margin_row = data.loc[data["Operating Margin (%)"].idxmax()]
    lowest_margin_row = data.loc[data["Operating Margin (%)"].idxmin()]

    revenue_change = latest_row["Revenue ($B)"] - earliest_row["Revenue ($B)"]
    income_change = latest_row["Net Income ($B)"] - earliest_row["Net Income ($B)"]
    margin_change = latest_row["Operating Margin (%)"] - earliest_row["Operating Margin (%)"]

    avg_revenue_growth = data["Revenue Growth (%)"].dropna().mean()
    avg_income_growth = data["Net Income Growth (%)"].dropna().mean()

    duplicate_rows = int(data.duplicated().sum())

    return {
        "latest_row": latest_row,
        "earliest_row": earliest_row,
        "highest_revenue_row": highest_revenue_row,
        "lowest_revenue_row": lowest_revenue_row,
        "highest_income_row": highest_income_row,
        "lowest_income_row": lowest_income_row,
        "highest_margin_row": highest_margin_row,
        "lowest_margin_row": lowest_margin_row,
        "revenue_change": revenue_change,
        "income_change": income_change,
        "margin_change": margin_change,
        "avg_revenue_growth": avg_revenue_growth,
        "avg_income_growth": avg_income_growth,
        "duplicate_rows": duplicate_rows
    }

def apply_common_layout(fig, title, x_title, y_title):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title="",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def render_download_button(dataframe, label, filename):
    st.download_button(
        label=label,
        data=to_csv_download(dataframe),
        file_name=filename,
        mime="text/csv"
    )

def render_glossary():
    with st.expander("Glossary: What do these metrics mean?"):
        st.markdown(
            """
            - **Revenue ($B):** total sales generated by the company.  
            - **Net Income ($B):** profit after expenses, interest, and taxes.  
            - **Operating Margin (%):** operating profit as a percentage of revenue.  
            - **Growth Rate (%):** year-to-year percentage change.  
            """
        )

# =========================================================
# Metrics
# =========================================================
metrics = get_metrics(df_filtered)

# =========================================================
# App header
# =========================================================
st.title("McDonald's Profitability Dashboard (2002–2022)")
st.write(
    "This interactive dashboard examines how McDonald's revenue, net income, and profitability changed over time."
)
st.caption("Data source: Kaggle McDonald's Financial Statements dataset | Access date: 2026-04-17")

if df_filtered.empty:
    st.error("No data is available for the selected year range. Please adjust the filter.")
    st.stop()

if show_data:
    st.subheader("Filtered Data")
    st.dataframe(df_filtered, use_container_width=True)

render_glossary()

# =========================================================
# Page functions
# =========================================================
def render_overview(data, metrics):
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
            **Selected period:** {int(data["Year"].min())} to {int(data["Year"].max())}

            **Number of years:** {len(data)}
            """
        )

    st.subheader("Key Metrics")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "Latest Revenue ($B)",
            fmt_billions(metrics["latest_row"]["Revenue ($B)"]),
            delta=f"{metrics['revenue_change']:.2f} vs start"
        )

    with kpi2:
        st.metric(
            "Latest Net Income ($B)",
            fmt_billions(metrics["latest_row"]["Net Income ($B)"]),
            delta=f"{metrics['income_change']:.2f} vs start"
        )

    with kpi3:
        st.metric(
            "Highest Revenue Year",
            f"{int(metrics['highest_revenue_row']['Year'])}"
        )

    with kpi4:
        st.metric(
            "Highest Operating Margin Year",
            f"{int(metrics['highest_margin_row']['Year'])}"
        )

    summary_fig = px.line(
        data,
        x="Year",
        y=["Revenue ($B)", "Net Income ($B)"],
        markers=True,
        color_discrete_sequence=[main_color, accent_color]
    )
    summary_fig = apply_common_layout(
        summary_fig,
        "Revenue and Net Income Over Time",
        "Year",
        "Value ($B)"
    )
    st.plotly_chart(summary_fig, use_container_width=True)

    if show_explanations:
        direction_rev = "increased" if metrics["revenue_change"] > 0 else "decreased"
        direction_income = "increased" if metrics["income_change"] > 0 else "decreased"

        st.markdown(
            f"""
            **Overview interpretation**  
            Across the selected period, revenue **{direction_rev} by {abs(metrics['revenue_change']):.2f} billion dollars**, 
            while net income **{direction_income} by {abs(metrics['income_change']):.2f} billion dollars**.  
            This suggests that business scale and profit performance did not always move at the same pace.
            """
        )

    st.subheader("Data Quality Snapshot")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("Missing Values (Filtered)", int(data.isna().sum().sum()))
    with d2:
        st.metric("Duplicate Rows (Filtered)", metrics["duplicate_rows"])
    with d3:
        st.metric("Columns", len(data.columns))


def render_full_data_overview(full_data, filtered_data):
    st.header("Full Data Overview")
    st.markdown(
        "This page provides a complete overview of the dataset, including structure, missing values, summary statistics, and the full data table."
    )

    st.subheader("Dataset Summary")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Rows", len(full_data))
    with c2:
        st.metric("Total Columns", len(full_data.columns))
    with c3:
        st.metric("Start Year", int(full_data["Year"].min()))
    with c4:
        st.metric("End Year", int(full_data["Year"].max()))

    st.markdown("---")

    st.subheader("Column Overview")
    column_info = pd.DataFrame({
        "Column Name": full_data.columns,
        "Data Type": full_data.dtypes.astype(str).values
    })
    st.dataframe(column_info, use_container_width=True)

    st.markdown("---")

    st.subheader("Missing Values")
    missing_values = full_data.isna().sum().reset_index()
    missing_values.columns = ["Column Name", "Missing Values"]
    st.dataframe(missing_values, use_container_width=True)

    st.markdown("---")

    st.subheader("Summary Statistics")
    numeric_cols = full_data.select_dtypes(include="number")
    if not numeric_cols.empty:
        st.dataframe(numeric_cols.describe().T, use_container_width=True)
    else:
        st.info("No numeric columns were found for summary statistics.")

    st.markdown("---")

    st.subheader("Full Dataset Table")
    st.dataframe(full_data, use_container_width=True)
    render_download_button(
        full_data,
        "Download Full Dataset as CSV",
        "mcdonalds_financial_data_full.csv"
    )

    st.markdown("---")

    st.subheader("Filtered Dataset Snapshot")
    st.write(
        f"The current year filter shows data from **{int(filtered_data['Year'].min())}** to **{int(filtered_data['Year'].max())}**."
    )
    st.dataframe(filtered_data, use_container_width=True)
    render_download_button(
        filtered_data,
        "Download Filtered Dataset as CSV",
        "mcdonalds_financial_data_filtered.csv"
    )


def render_revenue_page(data, metrics):
    st.header("Revenue Trend")
    st.markdown("**Question:** How did McDonald's business scale change over time?")

    fig_revenue = px.line(
        data,
        x="Year",
        y="Revenue ($B)",
        markers=True,
        color_discrete_sequence=[main_color]
    )
    fig_revenue = apply_common_layout(
        fig_revenue,
        "McDonald's Revenue Over Time",
        "Year",
        "Revenue ($B)"
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

    st.subheader("Revenue Growth Rate (%)")

    growth_note = st.checkbox("Show note about the first missing growth value", value=True, key="rev_note")
    if growth_note:
        st.caption("The first year has no growth rate because there is no previous year for comparison.")

    fig_growth = px.bar(
        data,
        x="Year",
        y="Revenue Growth (%)",
        color="Revenue Growth (%)",
        color_continuous_scale="RdYlGn"
    )
    fig_growth = apply_common_layout(
        fig_growth,
        "Year-to-Year Revenue Growth (%)",
        "Year",
        "Revenue Growth (%)"
    )
    fig_growth.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_growth, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "Highest Revenue ($B)",
            fmt_billions(metrics["highest_revenue_row"]["Revenue ($B)"]),
            f"Year {int(metrics['highest_revenue_row']['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Revenue ($B)",
            fmt_billions(metrics["lowest_revenue_row"]["Revenue ($B)"]),
            f"Year {int(metrics['lowest_revenue_row']['Year'])}"
        )
    with c3:
        avg_rev = metrics["avg_revenue_growth"]
        st.metric(
            "Average Revenue Growth",
            "N/A" if pd.isna(avg_rev) else fmt_percent(avg_rev)
        )

    if show_explanations:
        st.markdown(
            f"""
            **Revenue interpretation**  
            Revenue peaked in **{int(metrics['highest_revenue_row']['Year'])}** at **{metrics['highest_revenue_row']['Revenue ($B)']:.2f} billion dollars**.  
            The lowest revenue in the selected period was recorded in **{int(metrics['lowest_revenue_row']['Year'])}**.  
            The average revenue growth rate in the selected period was **{"N/A" if pd.isna(metrics['avg_revenue_growth']) else f"{metrics['avg_revenue_growth']:.2f}%"}**.  
            This suggests that McDonald's business scale changed over time rather than growing at a perfectly steady pace.
            """
        )


def render_income_page(data, metrics):
    st.header("Net Income Trend")
    st.markdown("**Question:** Did profit performance move in the same way as revenue?")

    fig_income = px.line(
        data,
        x="Year",
        y="Net Income ($B)",
        markers=True,
        color_discrete_sequence=[accent_color]
    )
    fig_income = apply_common_layout(
        fig_income,
        "McDonald's Net Income Over Time",
        "Year",
        "Net Income ($B)"
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
    fig_income_growth = apply_common_layout(
        fig_income_growth,
        "Year-to-Year Net Income Growth (%)",
        "Year",
        "Net Income Growth (%)"
    )
    fig_income_growth.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_income_growth, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "Highest Net Income ($B)",
            fmt_billions(metrics["highest_income_row"]["Net Income ($B)"]),
            f"Year {int(metrics['highest_income_row']['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Net Income ($B)",
            fmt_billions(metrics["lowest_income_row"]["Net Income ($B)"]),
            f"Year {int(metrics['lowest_income_row']['Year'])}"
        )
    with c3:
        avg_income = metrics["avg_income_growth"]
        st.metric(
            "Average Net Income Growth",
            "N/A" if pd.isna(avg_income) else fmt_percent(avg_income)
        )

    if show_explanations:
        st.markdown(
            f"""
            **Net income interpretation**  
            Net income reached its highest value in **{int(metrics['highest_income_row']['Year'])}** at **{metrics['highest_income_row']['Net Income ($B)']:.2f} billion dollars**, 
            and its lowest value in **{int(metrics['lowest_income_row']['Year'])}**.  
            The average net income growth rate in the selected period was **{"N/A" if pd.isna(metrics['avg_income_growth']) else f"{metrics['avg_income_growth']:.2f}%"}**.  
            Compared with revenue, profit performance appears more volatile, which means sales growth did not always translate into equally stable profit growth.
            """
        )


def render_profitability_page(data, metrics):
    st.header("Profitability Analysis")
    st.markdown("**Question:** Was McDonald's getting better at turning sales into profit?")

    fig_margin = px.line(
        data,
        x="Year",
        y="Operating Margin (%)",
        markers=True,
        color_discrete_sequence=[dark_color]
    )
    fig_margin = apply_common_layout(
        fig_margin,
        "Operating Margin Over Time",
        "Year",
        "Operating Margin (%)"
    )
    st.plotly_chart(fig_margin, use_container_width=True)

    compare_fig = px.line(
        data,
        x="Year",
        y=["Revenue ($B)", "Net Income ($B)"],
        markers=True,
        color_discrete_sequence=[main_color, accent_color]
    )
    compare_fig = apply_common_layout(
        compare_fig,
        "Revenue vs Net Income",
        "Year",
        "Value ($B)"
    )
    st.plotly_chart(compare_fig, use_container_width=True)

    st.subheader("Revenue vs Net Income Relationship")
    scatter_fig = px.scatter(
        data,
        x="Revenue ($B)",
        y="Net Income ($B)",
        color="Year",
        size="Operating Margin (%)",
        color_continuous_scale="YlOrRd",
        hover_data=["Year", "Operating Margin (%)"]
    )
    scatter_fig = apply_common_layout(
        scatter_fig,
        "Scatter Plot: Revenue vs Net Income",
        "Revenue ($B)",
        "Net Income ($B)"
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "Highest Margin (%)",
            f"{metrics['highest_margin_row']['Operating Margin (%)']:.2f}",
            f"Year {int(metrics['highest_margin_row']['Year'])}"
        )
    with c2:
        st.metric(
            "Lowest Margin (%)",
            f"{metrics['lowest_margin_row']['Operating Margin (%)']:.2f}",
            f"Year {int(metrics['lowest_margin_row']['Year'])}"
        )
    with c3:
        st.metric(
            "Margin Change",
            f"{metrics['margin_change']:.2f} pts"
        )

    if show_explanations:
        margin_direction = "improved" if metrics["margin_change"] > 0 else "declined"
        st.markdown(
            f"""
            **Why margin matters**  
            Operating margin shows how efficiently the company turns revenue into operating profit.  
            In the selected period, the highest operating margin appeared in **{int(metrics['highest_margin_row']['Year'])}** at **{metrics['highest_margin_row']['Operating Margin (%)']:.2f}%**, 
            while the lowest appeared in **{int(metrics['lowest_margin_row']['Year'])}**.  
            Overall, operating margin **{margin_direction} by {abs(metrics['margin_change']):.2f} percentage points** across the selected range, 
            showing whether profitability quality strengthened or weakened over time.

            **How to read the scatter plot**  
            Each circle represents one year.  
            The x-axis shows revenue, the y-axis shows net income, circle size shows operating margin, and color shows the year.  
            This helps users see whether higher revenue was consistently associated with stronger profit performance.
            """
        )

def render_insights_page(data, metrics):
    st.header("Key Insights & Limitations")

    st.subheader("Key Insights")

    start_year = int(metrics["earliest_row"]["Year"])
    end_year = int(metrics["latest_row"]["Year"])

    start_revenue = metrics["earliest_row"]["Revenue ($B)"]
    end_revenue = metrics["latest_row"]["Revenue ($B)"]

    start_income = metrics["earliest_row"]["Net Income ($B)"]
    end_income = metrics["latest_row"]["Net Income ($B)"]

    start_margin = metrics["earliest_row"]["Operating Margin (%)"]
    end_margin = metrics["latest_row"]["Operating Margin (%)"]

    revenue_peak_year = int(metrics["highest_revenue_row"]["Year"])
    revenue_low_year = int(metrics["lowest_revenue_row"]["Year"])

    income_peak_year = int(metrics["highest_income_row"]["Year"])
    income_low_year = int(metrics["lowest_income_row"]["Year"])

    margin_peak_year = int(metrics["highest_margin_row"]["Year"])
    margin_low_year = int(metrics["lowest_margin_row"]["Year"])

    revenue_direction = "increased" if metrics["revenue_change"] > 0 else "decreased"
    income_direction = "increased" if metrics["income_change"] > 0 else "decreased"
    margin_direction = "increased" if metrics["margin_change"] > 0 else "decreased"

    avg_rev_growth = metrics["avg_revenue_growth"]
    avg_income_growth = metrics["avg_income_growth"]

    same_peak = revenue_peak_year == income_peak_year

    st.markdown(
        f"""
        1. **Revenue {revenue_direction} from {start_revenue:.2f} billion dollars in {start_year} to {end_revenue:.2f} billion dollars in {end_year}.**  
           This shows that McDonald's business scale changed substantially across the selected period rather than remaining stable.

        2. **Net income {income_direction} from {start_income:.2f} billion dollars in {start_year} to {end_income:.2f} billion dollars in {end_year}.**  
           Compared with revenue, profit performance appears more volatile, which suggests that sales growth did not always translate into equally stable profit growth.

        3. **Revenue peaked in {revenue_peak_year}, while net income peaked in {income_peak_year}.**  
           {"Because these peak years are the same, strong sales and strong profit performance aligned in that period." if same_peak else "Because these peak years are different, the year with the highest sales was not necessarily the year with the strongest profit outcome."}

        4. **Operating margin {margin_direction} from {start_margin:.2f}% in {start_year} to {end_margin:.2f}% in {end_year}.**  
           The highest operating margin was recorded in {margin_peak_year}, while the lowest was recorded in {margin_low_year}.  
           This means McDonald's profitability quality changed over time rather than moving perfectly with business size alone.

        5. **The average revenue growth rate was {"N/A" if pd.isna(avg_rev_growth) else f"{avg_rev_growth:.2f}%"} and the average net income growth rate was {"N/A" if pd.isna(avg_income_growth) else f"{avg_income_growth:.2f}%"} in the selected period.**  
           This helps users compare growth in scale with growth in profit performance, which is more useful than looking at revenue only.

        6. **Overall, the dashboard suggests that larger revenue did not automatically mean stronger profitability in every year.**  
           For business students and potential investors, this highlights why revenue, net income, and operating margin should be interpreted together.
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
        Users can evaluate whether McDonald's growth was supported by stronger profit outcomes and operating efficiency, not just larger revenue numbers.
        """
    )

# =========================================================
# Page routing
# =========================================================
if page == "Overview":
    render_overview(df_filtered, metrics)

elif page == "Full Data Overview":
    render_full_data_overview(df, df_filtered)

elif page == "Revenue Trend":
    render_revenue_page(df_filtered, metrics)

elif page == "Net Income Trend":
    render_income_page(df_filtered, metrics)

elif page == "Profitability Analysis":
    render_profitability_page(df_filtered, metrics)

elif page == "Key Insights & Limitations":
    render_insights_page(df_filtered, metrics)

# =========================================================
# Footer
# =========================================================
st.markdown("---")
st.caption(
    "Educational use only. Figures are based on the selected dataset and should be interpreted as a simplified financial analysis tool."
)