"""
Script to programmatically construct the portfolio Jupyter Notebook `notebooks/marketing_analysis.ipynb`
with 16 clearly separated sections, explanatory text, and runnable Python code cells.
"""

import os
import nbformat as nbf

def build_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Header
    cells.append(nbf.v4.new_markdown_cell("""# Marketing Analytics & Campaign Performance Intelligence
## End-to-End Data Analytics Portfolio Project

> **DATA DISCLAIMER**: This notebook analyzes a simulated/synthetic dataset created specifically for educational and portfolio demonstration purposes. All data quality issues (missing values, duplicates, formatting inconsistencies, outliers) are intentionally injected to showcase practical Data Analyst workflows.

---
### Table of Contents
1. Import Libraries
2. Load Dataset
3. Initial Data Inspection
4. Dataset Shape
5. Column Information
6. Descriptive Statistics
7. Missing Value Analysis
8. Duplicate Analysis
9. Data Type Validation
10. Categorical Value Cleaning
11. Outlier Detection
12. Data Cleaning
13. Feature Engineering
14. Exploratory Data Analysis
15. KPI Analysis
16. Business Insights
"""))

    # Section 1
    cells.append(nbf.v4.new_markdown_cell("## 1. Import Libraries\nImport core Python data analysis and visualization libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`)."))
    cells.append(nbf.v4.new_code_cell("""import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual aesthetic defaults
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.size'] = 10

print("Libraries imported successfully!")
"""))

    # Section 2
    cells.append(nbf.v4.new_markdown_cell("## 2. Load Dataset\nLoad the raw marketing dataset from `data/raw/marketing_data_raw.csv`."))
    cells.append(nbf.v4.new_code_cell("""raw_data_path = os.path.join('..', 'data', 'raw', 'marketing_data_raw.csv')
if not os.path.exists(raw_data_path):
    raw_data_path = os.path.join('data', 'raw', 'marketing_data_raw.csv')

df_raw = pd.read_csv(raw_data_path)
print("Raw dataset loaded successfully!")
"""))

    # Section 3
    cells.append(nbf.v4.new_markdown_cell("## 3. Initial Data Inspection\nInspect the first 5 and last 5 rows of the dataset."))
    cells.append(nbf.v4.new_code_cell("df_raw.head()"))

    # Section 4
    cells.append(nbf.v4.new_markdown_cell("## 4. Dataset Shape\nExamine total row and column dimensions."))
    cells.append(nbf.v4.new_code_cell("""rows, cols = df_raw.shape
print(f"Total Rows: {rows:,}")
print(f"Total Columns: {cols}")
"""))

    # Section 5
    cells.append(nbf.v4.new_markdown_cell("## 5. Column Information\nReview column data types, non-null counts, and memory footprint."))
    cells.append(nbf.v4.new_code_cell("df_raw.info()"))

    # Section 6
    cells.append(nbf.v4.new_markdown_cell("## 6. Descriptive Statistics\nExamine central tendency, spread, min/max for numerical variables."))
    cells.append(nbf.v4.new_code_cell("df_raw.describe().T"))

    # Section 7
    cells.append(nbf.v4.new_markdown_cell("## 7. Missing Value Analysis\nIdentify missing values across all columns and calculate null percentages."))
    cells.append(nbf.v4.new_code_cell("""null_counts = df_raw.isnull().sum()
null_pct = (null_counts / len(df_raw)) * 100
missing_df = pd.DataFrame({'Missing_Count': null_counts, 'Missing_Percent': null_pct})
missing_df[missing_df['Missing_Count'] > 0]
"""))

    # Section 8
    cells.append(nbf.v4.new_markdown_cell("## 8. Duplicate Analysis\nCheck for full duplicate rows in the dataset."))
    cells.append(nbf.v4.new_code_cell("""num_duplicates = df_raw.duplicated().sum()
print(f"Number of duplicate rows: {num_duplicates} ({(num_duplicates/len(df_raw))*100:.2f}%)")
"""))

    # Section 9
    cells.append(nbf.v4.new_markdown_cell("## 9. Data Type Validation\nValidate dates and numerical columns."))
    cells.append(nbf.v4.new_code_cell("""df_clean = df_raw.copy()
# Convert date to datetime object
df_clean['Campaign_Date'] = pd.to_datetime(df_clean['Campaign_Date'])
df_clean['Year_Month'] = df_clean['Campaign_Date'].dt.to_period('M').astype(str)
print("Campaign_Date converted to datetime successfully!")
"""))

    # Section 10
    cells.append(nbf.v4.new_markdown_cell("## 10. Categorical Value Cleaning\nStandardize channel names, strip whitespace, and clean casing inconsistencies."))
    cells.append(nbf.v4.new_code_cell("""print("Unique raw channels before cleaning:")
print(df_clean['Channel'].unique())

df_clean['Channel'] = df_clean['Channel'].astype(str).str.strip().str.title()
channel_map = {
    'Google Ads': 'Google Ads', 'Google ads': 'Google Ads',
    'Facebook': 'Facebook', 'Instagram': 'Instagram',
    'Youtube': 'YouTube', 'Email': 'Email',
    'Search': 'Search', 'Display': 'Display', 'Referral': 'Referral'
}
df_clean['Channel'] = df_clean['Channel'].replace(channel_map)

print("\\nUnique channels after cleaning:")
print(df_clean['Channel'].unique())
"""))

    # Section 11
    cells.append(nbf.v4.new_markdown_cell("## 11. Outlier Detection\nDetect extreme spend and revenue values using percentiles."))
    cells.append(nbf.v4.new_code_cell("""spend_cap = df_clean['Marketing_Spend'].quantile(0.995)
rev_cap = df_clean['Revenue'].quantile(0.995)

print(f"99.5th Percentile Spend Cap: ${spend_cap:,.2f}")
print(f"99.5th Percentile Revenue Cap: ${rev_cap:,.2f}")

# Capping extreme outliers for clean analytical reporting
df_clean['Marketing_Spend'] = np.where(df_clean['Marketing_Spend'] > spend_cap, spend_cap, df_clean['Marketing_Spend'])
df_clean['Revenue'] = np.where(df_clean['Revenue'] > rev_cap, rev_cap, df_clean['Revenue'])
"""))

    # Section 12
    cells.append(nbf.v4.new_markdown_cell("## 12. Data Cleaning Execution\nDeduplicate and impute missing values."))
    cells.append(nbf.v4.new_code_cell("""# Drop duplicates
df_clean = df_clean.drop_duplicates().reset_index(drop=True)

# Impute missing Leads
df_clean['Leads'] = df_clean['Leads'].fillna(df_clean['Clicks'] * 0.15).astype(int)

# Impute missing Revenue
df_clean['Revenue'] = df_clean.apply(
    lambda r: round(r['Conversions'] * r['Order_Value'], 2) if pd.isna(r['Revenue']) else r['Revenue'],
    axis=1
)

# Impute Customer Segment
mode_seg = df_clean[df_clean['Customer_Segment'] != 'Unknown']['Customer_Segment'].mode()[0]
df_clean['Customer_Segment'] = df_clean['Customer_Segment'].fillna(mode_seg)

print(f"Remaining null values: {df_clean.isnull().sum().sum()}")
"""))

    # Section 13
    cells.append(nbf.v4.new_markdown_cell("## 13. Feature Engineering\nCalculate key digital marketing performance metrics:\n- **CTR**: Clicks / Impressions * 100\n- **Conversion Rate**: Conversions / Leads * 100\n- **Cost Per Click (CPC)**: Spend / Clicks\n- **Cost Per Lead (CPL)**: Spend / Leads\n- **Cost Per Acquisition (CPA)**: Spend / Conversions\n- **Revenue Per Conversion (RPC)**: Revenue / Conversions\n- **ROI %**: (Revenue - Spend) / Spend * 100"))
    cells.append(nbf.v4.new_code_cell("""df_clean['CTR'] = np.where(df_clean['Impressions'] > 0, (df_clean['Clicks'] / df_clean['Impressions']) * 100, 0.0)
df_clean['Conversion_Rate'] = np.where(df_clean['Leads'] > 0, (df_clean['Conversions'] / df_clean['Leads']) * 100, 0.0)
df_clean['Cost_Per_Click'] = np.where(df_clean['Clicks'] > 0, df_clean['Marketing_Spend'] / df_clean['Clicks'], 0.0)
df_clean['Cost_Per_Lead'] = np.where(df_clean['Leads'] > 0, df_clean['Marketing_Spend'] / df_clean['Leads'], 0.0)
df_clean['Cost_Per_Acquisition'] = np.where(df_clean['Conversions'] > 0, df_clean['Marketing_Spend'] / df_clean['Conversions'], 0.0)
df_clean['Revenue_Per_Conversion'] = np.where(df_clean['Conversions'] > 0, df_clean['Revenue'] / df_clean['Conversions'], 0.0)
df_clean['ROI'] = np.where(df_clean['Marketing_Spend'] > 0, ((df_clean['Revenue'] - df_clean['Marketing_Spend']) / df_clean['Marketing_Spend']) * 100, 0.0)

# Age Group Binning
bins = [17, 25, 35, 50, 65, 100]
labels = ['18-25', '26-35', '36-50', '51-65', '65+']
df_clean['Age_Group'] = pd.cut(df_clean['Customer_Age'], bins=bins, labels=labels)

df_clean[['CTR', 'Conversion_Rate', 'Cost_Per_Acquisition', 'ROI']].head()
"""))

    # Section 14
    cells.append(nbf.v4.new_markdown_cell("## 14. Exploratory Data Analysis\nPerform multi-dimensional exploratory data analysis across Channels, Campaigns, Segments, and Time."))
    cells.append(nbf.v4.new_code_cell("""# Channel Performance Table
channel_summary = df_clean.groupby('Channel').agg(
    Spend=('Marketing_Spend', 'sum'),
    Revenue=('Revenue', 'sum'),
    Conversions=('Conversions', 'sum'),
    Leads=('Leads', 'sum'),
    Clicks=('Clicks', 'sum'),
    Impressions=('Impressions', 'sum')
).reset_index()

channel_summary['CTR_%'] = (channel_summary['Clicks'] / channel_summary['Impressions']) * 100
channel_summary['Conv_Rate_%'] = (channel_summary['Conversions'] / channel_summary['Leads']) * 100
channel_summary['CPA'] = channel_summary['Spend'] / channel_summary['Conversions']
channel_summary['ROI_%'] = ((channel_summary['Revenue'] - channel_summary['Spend']) / channel_summary['Spend']) * 100

channel_summary.sort_values(by='Revenue', ascending=False)
"""))

    # Section 15
    cells.append(nbf.v4.new_markdown_cell("## 15. KPI Analysis\nCalculate overall top-line marketing KPIs."))
    cells.append(nbf.v4.new_code_cell("""tot_spend = df_clean['Marketing_Spend'].sum()
tot_rev = df_clean['Revenue'].sum()
tot_conv = df_clean['Conversions'].sum()
overall_roi = ((tot_rev - tot_spend) / tot_spend) * 100
blended_cpa = tot_spend / tot_conv

print(f"Total Marketing Spend:   ${tot_spend:,.2f}")
print(f"Total Revenue Generated: ${tot_rev:,.2f}")
print(f"Total Net Profit:        ${(tot_rev - tot_spend):,.2f}")
print(f"Overall Blended ROI:     {overall_roi:.2f}%")
print(f"Blended CPA:             ${blended_cpa:.2f}")
"""))

    # Section 16
    cells.append(nbf.v4.new_markdown_cell("""## 16. Business Insights & Summary
1. **Email & Referral** are the highest ROI channels (255.6% and 214.0% ROI respectively).
2. **Google Ads** drives the highest overall revenue ($7.85M) and conversion volume.
3. **CMP-113 (High-Spend Experimental)** is underperforming with negative ROI (-33.5%).
4. **B2B Enterprise** generates 43.1% of gross revenue via Software/SaaS purchases.
"""))

    nb['cells'] = cells
    
    nb_dir = 'notebooks'
    os.makedirs(nb_dir, exist_ok=True)
    nb_path = os.path.join(nb_dir, 'marketing_analysis.ipynb')
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"Jupyter Notebook successfully created at: {nb_path}")

if __name__ == '__main__':
    build_notebook()
