# PhonePe-Pulse-Data-Insights-and-Prediction-Dashboard
## 📊 PhonePe Pulse Insights Dashboard
An end-to-end interactive dashboard project analyzing India's digital payment behavior using PhonePe Pulse data. The project includes exploratory data analysis, visualizations, and machine learning models to generate actionable insights for stakeholders.

## 🚀 Project Title
PhonePe Pulse Data Insights and Prediction Dashboard

## 💡 Problem Statement
PhonePe has rapidly expanded across India, enabling millions to access digital financial services. However, understanding usage patterns, insurance adoption, and regional disparities requires in-depth analytics.

This project aims to:
  - Analyze and visualize state/district-wise trends in transactions, user engagement, and insurance uptake.
  - Identify behavioral patterns in device usage and app engagement.
  - Predict app opens and user activity using machine learning models.

## 🗃️ Data Source
📂 Source: PhonePe Pulse GitHub Repository

Raw data is organized in JSON format under categories:

aggregated/insurance

aggregated/transaction

aggregated/user

map/user

##  🧰 Tools and Technologies Used
Python 3.11

SQLite3 – for structured data storage

Pandas – data preprocessing and manipulation

Plotly & Matplotlib – data visualizations

Streamlit – dashboard interface

Scikit-learn & XGBoost – machine learning modeling

Jupyter Notebook – analysis & EDA

## 📈 Key Insights
Insurance Trends: Maharashtra and Karnataka lead in digital insurance amount.

Transaction Patterns: P2M (Person to Merchant) transactions dominate across states.

Device Usage: Xiaomi and Samsung are top-used brands; however, iPhone users show higher app open ratios.

App Usage Prediction: ML models (Linear, RF, XGB) show high accuracy in predicting app opens based on user registration and district trends.

Data Quality: Some newer data (e.g., 2024) had null fields or partial entries.

## 🛠️ How to Run the Project Locally
1. Clone the Repository
git clone https://github.com/SuziSharma2/phonepe-insights.git
cd phonepe-insights
2. Set up a Virtual Environment (optional but recommended)
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On macOS/Linux
3. Install Dependencies
pip install -r requirements.txt
4. Run the Streamlit Dashboard
streamlit run streamlit_app/app.py
5. Open in Browser
Once started, the dashboard URL (typically http://localhost:8501) will open in your default browser.

## 📁 Project Structure
```
phonepe-insights/
│
├── README.md                      <- ✅ Project overview, setup steps, insights summary
├── requirements.txt              <- ✅ All necessary libraries (for pip install)
├── .gitignore                    <- Ignore `__pycache__/`, `.db`, `.ipynb_checkpoints/`
│
├── 📁 data/                       <- Raw & processed data
│   └── 📁 aggregated/
│       ├── 📁 insurance/
│       ├── 📁 transaction/
│       └── 📁 user/
│   └── 📁 map/
│       └── 📁 user/
│
├── 📁 db/
│   └── phonepe_data.db           <- Final SQLite database
│
├── 📁 scripts/                   <- Python scripts for table creation & data loading
│   ├── create_all_tables.py
│   ├── load_aggregated_insurance.py
│   ├── load_aggregated_transactions.py
│   ├── load_aggregated_user.py
│   └── load_map_user.py
│
├── 📁 notebooks/                 <- Jupyter notebooks for EDA, visualizations, ML
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_visuals.ipynb
│   ├── 03_hypothesis_testing.ipynb
│   └── 04_ml_modeling.ipynb
│
├── 📁 streamlit_app/             <- Streamlit dashboard files
│   └── app.py                    <- Main dashboard script
│
└── 📁 reports/                   <- Final project report & summary
    ├── project_summary.pdf
    └── insights_ppt.pptx

```
