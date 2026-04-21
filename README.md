# McDonald's Profitability Dashboard (2002–2022)

**ACC102 Mini Assignment – Track 4**

## Product Links
- **GitHub Repository:** https://github.com/JiayiWu2404/acc102-mcdonalds-dashboard
- **App Link:** Not deployed
- **Demo Video (1–3 minutes):** [Paste your Mediasite video link here]

## Project Overview
This project is an interactive Streamlit dashboard that analyses how McDonald's financial performance changed from 2002 to 2022.

The dashboard focuses on three key indicators:
- **Revenue**
- **Net Income**
- **Operating Margin**

It helps users explore whether long-term revenue growth was matched by stronger profitability over time.

## Research Question
**Did McDonald's long-term revenue growth translate into stronger profitability from 2002 to 2022?**

## Target Users
This dashboard is designed for:
- potential investors
- industry analysts
- business students
- users interested in restaurant industry performance

## Data Source
- **Dataset:** `McDonalds_Financial_Statements.csv`
- **Source:** Public McDonald's financial statements dataset from Kaggle
- **Access Date:** [Insert your access date here]

The dataset is included in this repository for reproducibility.

## Main Features
- interactive year range filter
- multi-page dashboard layout
- revenue trend analysis
- net income trend analysis
- operating margin analysis
- summary metrics and written insights
- optional filtered data table display

## How to Run the App Locally
Install the required packages:

```bash
pip install -r requirements.txt

Run the Streamlit app:
Bash
streamlit run app.py
After running the command, the dashboard should open in your browser.
Required Packages
Txt
streamlit
pandas
plotly
Files Included
app.py – main Streamlit dashboard
requirements.txt – required Python packages
notebook.ipynb – notebook showing data loading, cleaning, analysis, and outputs
data/McDonalds_Financial_Statements.csv – dataset used in the project
README.md – project documentation
Repository Structure
Text
acc102-mcdonalds-dashboard/
│
├── README.md
├── app.py
├── requirements.txt
├── notebook.ipynb
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
improving error handling and validation
enhancing the interface design and user experience
Disclaimer
This dashboard is for educational use only.
It is based on a public dataset and should be interpreted as a simplified financial analysis tool rather than investment advice.
