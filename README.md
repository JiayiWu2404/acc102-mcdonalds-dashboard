# McDonald's Profitability Dashboard (2002–2022)

**ACC102 Mini Assignment – Track 4: Interactive Data Analysis Tool**

## Product Links

- **GitHub Repository:** https://github.com/JiayiWu2404/acc102-mcdonalds-dashboard
- **App Link:** https://acc102-mcdonalds-dashboard-imnjvadkhuxqcc3czza6ec.streamlit.app/
- **Demo Video (1–3 minutes):** https://video.xjtlu.edu.cn/Mediasite/MyMediasite/embedded/presentations/da74914b77404460a018fbcac61326b71d

---

## Project Overview

This project is an interactive Streamlit dashboard that analyses how McDonald’s financial performance changed from 2002 to 2022.

The dashboard focuses on three core indicators:

- **Revenue**
- **Net Income**
- **Operating Margin**

Its main purpose is to help users evaluate whether McDonald’s long-term revenue growth was supported by stronger profitability over time, rather than simply larger business scale.

---

## Research Question

**Did McDonald’s long-term revenue growth translate into stronger profitability from 2002 to 2022?**

To answer this question, the dashboard focuses on three related aspects:

1. How did McDonald’s revenue change over time?
2. Did net income move in the same way as revenue?
3. Was McDonald’s getting better at turning sales into profit?

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

This dashboard helps users evaluate McDonald’s performance from multiple angles by comparing:

- business scale through revenue
- profit performance through net income
- efficiency through operating margin

For investors, students, and industry observers, this is useful because revenue alone may be an incomplete indicator of long-term business quality.

---

## Main Features

This dashboard includes:

- an interactive year range filter
- a multi-page dashboard layout
- an **Overview** page with project context, KPI cards, a quick summary, and usage guidance
- a **Full Data Overview** page showing dataset structure, missing values, and summary statistics
- a **Revenue Trend** page with revenue growth analysis
- a **Net Income Trend** page with net income growth analysis
- a **Profitability Analysis** page using operating margin and comparative charts
- a **Metric Comparison** page with metric selection and two-period comparison
- a **Key Insights & Limitations** page with written interpretations
- an optional filtered data table display
- downloadable full dataset and filtered dataset outputs
- basic error handling for missing files, empty data, and missing required columns

---

## How to Use the Dashboard

Users can interact with the dashboard through the sidebar.

Main actions include:

- selecting a year range
- navigating between dashboard pages
- viewing filtered data
- downloading the full dataset or filtered dataset

Recommended page order:

1. **Overview** – understand the research question, users, quick summary, and key metrics
2. **Revenue Trend** – understand business scale
3. **Net Income Trend** – assess profit stability
4. **Profitability Analysis** – evaluate efficiency and margin quality
5. **Metric Comparison** – compare indicators and compare two selected periods
6. **Key Insights & Limitations** – review the main conclusions and project boundaries

This structure helps users move from description to interpretation rather than only viewing isolated charts.

---

## Data Source

- **Dataset:** `McDonalds_Financial_Statements.csv`
- **Source:** Public McDonald’s financial statements dataset from Kaggle
- **Access Date:** 17 April 2026

The dataset is included in this repository for reproducibility.

I selected this dataset because it includes key indicators such as revenue, net income, and operating margin across multiple years. These variables are suitable for analysing business scale, profit performance, and profitability quality in a business-related context.

---

## Data Preparation

The dataset was already relatively clean and structured.  
The following light data preparation steps were applied in Python:

- standardising column names
- validating required columns
- renaming one variable for consistency
- sorting the dataset by year
- calculating revenue growth and net income growth
- checking missing values and summary statistics
- recalculating growth indicators after year-range filtering

These preparation steps helped ensure that the dashboard was not only visual, but also analytically meaningful.

---

## Methods

This project was built using:

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**

The main analytical workflow was:

1. Load the dataset using a relative path
2. Validate the data structure and required columns
3. Prepare and organise the data
4. Calculate derived indicators such as growth rates
5. Apply year-range filtering
6. Generate interactive charts, key metrics, and comparisons
7. Present insights, limitations, and downloadable outputs in a dashboard format

This workflow supports the final tool by combining Python-based data preparation, descriptive analysis, visualisation, comparison logic, and interpretation.

---

## Dashboard Pages

### 1. Overview
Provides the research question, target users, selected period, quick summary, how-to-use guidance, key metrics, and a summary chart of revenue and net income.

### 2. Full Data Overview
Shows dataset structure, column types, missing values, summary statistics, and full/filtered data tables.

### 3. Revenue Trend
Shows how McDonald’s revenue changed over time and includes year-to-year revenue growth.

### 4. Net Income Trend
Shows how net income changed over time and compares profit movement with revenue growth.

### 5. Profitability Analysis
Uses operating margin and comparative charts to evaluate whether McDonald’s became more effective at converting sales into profit.

### 6. Metric Comparison
Allows users to select an indicator and compare performance across two different time periods.

### 7. Key Insights & Limitations
Summarises the main findings, project limitations, and possible future improvements.

---

## Key Findings

The dashboard suggests that:

- McDonald’s revenue changed substantially over the selected period rather than growing at a perfectly steady pace.
- Net income was more volatile than revenue, which suggests that sales growth did not always translate into equally stable profit growth.
- The year with the highest revenue was not necessarily the year with the strongest profit performance.
- Operating margin changed over time, showing that profitability quality did not move perfectly with business scale alone.
- Revenue, net income, and operating margin should be interpreted together rather than in isolation.

From a business perspective, this means that revenue expansion alone may be an incomplete indicator of business quality.  
For investors, students, and industry observers, a more meaningful evaluation should also consider profit stability and operating efficiency.

---

## Error Handling and Reproducibility

The app includes basic validation to improve robustness and reproducibility.  
For example, it checks whether:

- the dataset file exists in the correct folder
- the CSV file can be read successfully
- the dataset is empty
- required columns are present
- the selected year range returns valid data

This helps ensure that the repository can be run more reliably after cloning.

---

## How to Run the App Locally


```bash
1. Install the required packages

pip install -r requirements.txt
2. Run the Streamlit app
streamlit run app.py

After running the command, the dashboard should open in your browser.

This repository is designed so that the app can be run locally after cloning, as long as the required packages are installed and the dataset remains in the data folder.

Required Packages

The project uses the following Python packages:

streamlit
pandas
plotly
Files Included
app.py – main Streamlit dashboard
requirements.txt – required Python packages
data/McDonalds_Financial_Statements.csv – dataset used in the project
README.md – project documentation
Repository Structure
acc102-mcdonalds-dashboard/
│
├── README.md
├── app.py
├── notebook.ipynb
├── requirements.txt
└── data/
    └── McDonalds_Financial_Statements.csv
Limitations

This project has several limitations:

it focuses on one company only
it does not include competitor comparison
it depends on the accuracy and completeness of the public dataset
it does not directly model external business events
it uses selected financial indicators only and is not a full valuation model
Future Improvements

Possible future improvements include:

adding competitor comparison such as Starbucks or Yum! Brands
adding more financial ratios and indicators
adding business event annotations to the charts
improving error handling and validation further
enhancing the interface design and user experience
adding stronger metric comparison options and user-controlled toggles
Demo Video Guidance

The demo video should show more than the final dashboard interface.
It should also demonstrate that the main workflow can run and that the project structure is understandable.

The video should ideally include:

a brief introduction to the research question
a short explanation of the dataset
a demonstration of the dashboard pages
an explanation of one or two key insights
a brief view of the repository structure and main files
a short demonstration of running streamlit run app.py
Disclaimer

This dashboard is for educational use only.
It is based on a public dataset and should be interpreted as a simplified financial analysis tool rather than investment advice.
