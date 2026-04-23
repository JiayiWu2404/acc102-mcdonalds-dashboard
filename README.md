# McDonald's Profitability Dashboard (2002–2022)

**ACC102 Mini Assignment – Track 4: Interactive Data Analysis Tool**

## Product Links

- **GitHub Repository:** https://github.com/JiayiWu2404/acc102-mcdonalds-dashboard
- **App Link:** https://acc102-mcdonalds-dashboard-imnjvadkhuxqcc3czza6ec.streamlit.app/
- **Demo Video (1–3 minutes):** [Paste your Mediasite video link here]

---

## Project Overview

This project is an interactive Streamlit dashboard that analyses how McDonald's financial performance changed from 2002 to 2022.

The dashboard focuses on three core indicators:

- **Revenue**
- **Net Income**
- **Operating Margin**

It helps users explore whether McDonald's long-term revenue growth was supported by stronger profitability over time.

---

## Research Question

**Did McDonald's long-term revenue growth translate into stronger profitability from 2002 to 2022?**

To answer this question, the dashboard focuses on three related aspects:

1. How did McDonald's revenue change over time?
2. Did net income move in the same way as revenue?
3. Was McDonald's getting better at turning sales into profit?

---

## Target Users

This dashboard is designed for:

- potential investors
- industry analysts
- business students
- users interested in restaurant industry performance

---

## Why This Project Matters

Revenue growth alone does not always mean stronger business performance.  
A company may generate higher sales without improving profitability quality.

This dashboard helps users evaluate McDonald's performance from multiple angles by comparing:

- business scale through revenue
- profit performance through net income
- efficiency through operating margin

---

## Main Features

This dashboard includes:

- an **interactive year range filter**
- a **multi-page dashboard layout**
- an **Overview** page with project context and KPI cards
- a **Full Data Overview** page showing dataset structure, missing values, and summary statistics
- a **Revenue Trend** page with revenue growth analysis
- a **Net Income Trend** page with net income growth analysis
- a **Profitability Analysis** page using operating margin and comparative charts
- a **Key Insights & Limitations** page with written interpretations
- an optional **filtered data table display**
- downloadable **full dataset** and **filtered dataset** outputs

---

## Data Source

- **Dataset:** `McDonalds_Financial_Statements.csv`
- **Source:** Public McDonald's financial statements dataset from Kaggle
- **Access Date:** [Insert your access date here]

The dataset is included in this repository for reproducibility.

---

## Data Preparation

The dataset was already relatively clean and structured.  
The following light data preparation steps were applied in Python:

- standardising column names
- renaming one variable for consistency
- sorting the dataset by year
- calculating revenue growth and net income growth
- checking missing values and summary statistics
- recalculating growth indicators after year-range filtering

---

## Methods

This project was built using:

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**

The main workflow was:

1. Load the dataset
2. Prepare and organise the data
3. Calculate derived indicators such as growth rates
4. Apply year-range filtering
5. Generate interactive charts and key metrics
6. Present insights, limitations, and downloadable outputs in a dashboard format

---

## Dashboard Pages

### 1. Overview
Provides the research question, target users, selected period, key metrics, and a summary chart of revenue and net income.

### 2. Full Data Overview
Shows the dataset structure, column types, missing values, summary statistics, and full/filtered data tables.

### 3. Revenue Trend
Shows how McDonald's revenue changed over time and includes year-to-year revenue growth.

### 4. Net Income Trend
Shows how net income changed over time and compares profit movement with revenue growth.

### 5. Profitability Analysis
Uses operating margin and comparative charts to evaluate whether McDonald's became more effective at converting sales into profit.

### 6. Key Insights & Limitations
Summarises the main findings, project limitations, and possible future improvements.

---

## Key Findings

The dashboard suggests that:

- McDonald's revenue changed substantially over the selected period rather than growing at a perfectly steady pace.
- Net income was more volatile than revenue, which suggests that sales growth did not always translate into equally stable profit growth.
- The year with the highest revenue was not necessarily the year with the strongest profit performance.
- Operating margin changed over time, showing that profitability quality did not move perfectly with business scale alone.
- Revenue, net income, and operating margin should be interpreted together rather than in isolation.

---

## How to Run the App Locally

### 1. Install the required packages

```bash
pip install -r requirements.txt
2. Run the Streamlit app
Bash
￼
streamlit run app.py
After running the command, the dashboard should open in your browser.
￼
Required Packages
The project uses the following Python packages:
streamlit
pandas
plotly
￼
Files Included
• app.py – main Streamlit dashboard
• requirements.txt – required Python packages
• notebook.ipynb – notebook showing data loading, preparation, analysis, and outputs
• data/McDonalds_Financial_Statements.csv – dataset used in the project
• README.md – project documentation
￼
Repository Structure
acc102-mcdonalds-dashboard/
│
├── README.md
├── app.py
├── requirements.txt
├── notebook.ipynb
└── data/
    └── McDonalds_Financial_Statements.csv
￼
Limitations
This project has several limitations:
• it focuses on one company only
• it does not include competitor comparison
• it depends on the accuracy and completeness of the public dataset
• it does not directly model external business events
• it uses selected financial indicators only and is not a full valuation model
￼
Future Improvements
Possible future improvements include:
• adding competitor comparison such as Starbucks or Yum! Brands
• adding more financial ratios and indicators
• adding business event annotations to the charts
• improving error handling and validation
• enhancing the interface design and user experience
￼
Demo Video Guidance
The demo video should show more than the final dashboard interface.
It should also demonstrate that the main workflow can run and that the project structure is understandable.
The video should ideally include:
• a brief introduction to the research question
• a short explanation of the dataset
• a demonstration of the dashboard pages
• an explanation of one or two key insights
• a brief view of the repository structure and main files
￼
Disclaimer
This dashboard is for educational use only.
It is based on a public dataset and should be interpreted as a simplified financial analysis tool rather than investment advice.
