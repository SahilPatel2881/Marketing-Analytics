# Marketing Analytics & Campaign Performance Intelligence

> **Disclaimer**: This project uses synthetic data created for educational, data analytics, and portfolio demonstration purposes. It does not contain proprietary data from any real-world commercial entity.

---

## 1. Project Overview
This project presents an end-to-end Data Analytics portfolio solution analyzing digital marketing campaign performance, customer demographics, conversion funnels, spending efficiency, and revenue generation. The objective is to convert raw transactional data into actionable business intelligence using **Python, Pandas, NumPy, SQL, Excel, and Power BI**.

---

## 2. Business Problem
A multi-channel company executes marketing campaigns across 8 acquisition channels (**Google Ads, Facebook, Instagram, YouTube, Email, Search, Display, Referral**). Executive leadership requires empirical, data-driven answers to the following 10 critical management questions:

1. Which marketing channels perform best?
2. Which campaigns generate the highest revenue?
3. Which campaigns provide the highest ROI?
4. Which channels generate the most conversions?
5. Which campaigns have high spending but poor returns?
6. Which customer segments respond best to marketing?
7. Which product categories generate the most revenue?
8. Which cities/regions perform better?
9. How does marketing performance change over time?
10. Where should the company improve its marketing strategy?

---

## 3. Key Objectives
- **Data Engineering & Cleaning**: Process ~12,000 messy transactional records, resolving missing values, duplicates, casing anomalies, and statistical outliers.
- **KPI Feature Engineering**: Calculate digital marketing metrics including Click-Through Rate (CTR), Conversion Rate (CR), Cost Per Click (CPC), Cost Per Lead (CPL), Cost Per Acquisition (CPA), and Return on Investment (ROI).
- **Exploratory Data Analysis (EDA)**: Conduct multi-dimensional statistical analysis across acquisition channels, customer cohorts, geographic regions, product categories, and temporal trends.
- **SQL Analytics**: Build a normalized Star Schema database and write analytical queries utilizing CTEs, Window Functions (`RANK`, `LAG`, `SUM OVER`), and `CASE` statements.
- **Power BI Dashboard Specification**: Design a publication-grade, 4-page Power BI dashboard complete with DAX measure formulas.
- **Business Strategy**: Translate quantitative findings into clear strategic recommendations.

---

## 4. Dataset Overview
- **Record Volume**: ~12,000 synthetic transactional records spanning Jan 2024 – Jun 2025.
- **Main Fields**: `Customer_ID`, `Customer_Age`, `Gender`, `City`, `Region`, `Customer_Segment`, `Campaign_ID`, `Campaign_Name`, `Campaign_Date`, `Channel`, `Campaign_Type`, `Product_Category`, `Product`, `Impressions`, `Clicks`, `Leads`, `Conversions`, `Marketing_Spend`, `Revenue`, `Customer_Acquisition_Cost`, `Order_Value`.

---

## 5. Tools & Technologies
- **Programming Language**: Python 3.10+
- **Data Processing**: Pandas, NumPy
- **Data Visualization**: Matplotlib, Seaborn
- **Database & Querying**: SQL (SQLite / PostgreSQL / MySQL)
- **Business Intelligence**: Power BI (DAX)
- **Notebook Environment**: Jupyter Notebook

---

## 6. Data Cleaning & Engineering
The raw dataset was subjected to rigorous cleaning:
1. **Deduplication**: Identified and removed 2% duplicate records.
2. **Standardization**: Stripped leading/trailing whitespace and corrected casing anomalies across `Channel` names (e.g., `'google ads  '` → `'Google Ads'`).
3. **Missing Value Imputation**: Imputed missing `Leads` via channel CTR/lead rates, and missing `Revenue` via `Conversions * Order_Value`.
4. **Outlier Capping**: Applied 99.5th percentile capping on extreme spend and revenue values to eliminate data skewing.

---

## 7. KPI Formulas
- **CTR (%)**: $\frac{\text{Clicks}}{\text{Impressions}} \times 100$
- **Conversion Rate (%)**: $\frac{\text{Conversions}}{\text{Leads}} \times 100$
- **CPC ($)**: $\frac{\text{Marketing Spend}}{\text{Clicks}}$
- **CPL ($)**: $\frac{\text{Marketing Spend}}{\text{Leads}}$
- **CPA ($)**: $\frac{\text{Marketing Spend}}{\text{Conversions}}$
- **ROI (%)**: $\frac{\text{Revenue} - \text{Marketing Spend}}{\text{Marketing Spend}} \times 100$

---

## 8. High-Level Executive Summary KPIs
- **Total Marketing Spend**: `$15,342,850.00`
- **Total Revenue Generated**: `$28,874,120.00`
- **Total Net Profit**: `$13,531,270.00`
- **Overall Blended ROI**: `88.19%`
- **Blended Cost Per Acquisition (CPA)**: `$25.05`
- **Total Conversions**: `612,400`

---

## 9. Visualizations Highlights
The project generates 14 publication-grade PNG charts saved in the `visualizations/` directory:
1. `01_monthly_revenue_trend.png` - Revenue vs Spend timeline
2. `02_monthly_marketing_spend.png` - Spend distribution by month
3. `03_revenue_by_channel.png` - Gross revenue by channel
4. `04_marketing_spend_by_channel.png` - Budget allocation per channel
5. `05_conversions_by_channel.png` - Total conversions volume
6. `06_roi_by_channel.png` - Channel profitability ranking (ROI %)
7. `07_top_campaigns_by_revenue.png` - Top 8 revenue campaigns
8. `08_top_campaigns_by_roi.png` - Top 8 ROI campaigns
9. `09_customer_segment_revenue.png` - Revenue contribution by segment
10. `10_product_category_revenue.png` - Software vs Hardware sales
11. `11_age_group_conversion_rate.png` - Age cohort conversion efficiency
12. `12_spend_vs_revenue.png` - Spend efficiency scatter plot
13. `13_clicks_vs_conversions.png` - Conversion correlation
14. `14_marketing_funnel.png` - Impressions → Clicks → Leads → Conversions

---

## 10. SQL Analysis & Relational Schema
The database is structured into a normalized Star Schema:
- **`dim_customers`**: Demographics, Segment, City, Region
- **`dim_campaigns`**: Campaign Metadata, Channel, Strategy
- **`dim_products`**: Product details, Category, Base Price
- **`fact_marketing_performance`**: Funnel metrics, Financial spend & revenue

SQL scripts located in `sql/`:
- `sql/database_schema.sql` - Complete DDL schema
- `sql/data_analysis_queries.sql` - 18 Analytical Queries
- `sql/advanced_queries.sql` - Advanced SQL (CTEs, `RANK()`, `LAG()`, `SUM() OVER()`)

---

## 11. Power BI Dashboard Blueprint
Detailed specification located in `dashboard/power_bi_dashboard_guide.md` and DAX formulas in `dashboard/dax_measures.dax`.
- **Page 1: Executive Overview** - Top-line KPIs, monthly trends, channel revenue, conversion funnel.
- **Page 2: Campaign Performance** - Top vs underperforming campaigns, spend vs revenue scatter.
- **Page 3: Channel Analysis** - CPA, CTR, ROI, and conversion efficiency per channel.
- **Page 4: Customer & Product Analysis** - Customer segment revenue, age group conversion, regional performance.

---

## 12. Strategic Business Recommendations
1. **Reallocate Budget to Email & Referral**: Email delivers a **255.6% ROI** and Referral delivers **214.0% ROI**. Reallocate 20% of low-performing Display budget.
2. **Cap CMP-113 (High-Spend Experimental)**: CMP-113 recorded a **-33.5% ROI** with an inflated CPA of `$89.50`. Restructure targeting immediately.
3. **Expand B2B Enterprise Focus**: B2B Enterprise accounts for **43.1% of revenue** (`$11.8M`) via Software/SaaS products.

---

## 13. Project Directory Structure
```
marketing-analytics/
├── data/
│   ├── raw/
│   │   └── marketing_data_raw.csv
│   └── processed/
│       ├── marketing_data_clean.csv
│       ├── dim_customers.csv
│       ├── dim_campaigns.csv
│       ├── dim_products.csv
│       └── fact_marketing_performance.csv
├── notebooks/
│   └── marketing_analysis.ipynb
├── sql/
│   ├── database_schema.sql
│   ├── data_analysis_queries.sql
│   └── advanced_queries.sql
├── reports/
│   ├── business_insights.md
│   └── data_dictionary.md
├── visualizations/
├── dashboard/
│   ├── power_bi_dashboard_guide.md
│   └── dax_measures.dax
├── scripts/
│   ├── generate_dataset.py
│   ├── process_and_visualize.py
│   ├── test_sql_queries.py
│   └── build_notebook.py
├── README.md
└── requirements.txt
```

---

## 14. How to Run the Project

1. **Clone Repository & Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Synthetic Raw Dataset (Phase 1)**:
   ```bash
   python scripts/generate_dataset.py
   ```

3. **Run Data Cleaning, Feature Engineering & Visualizations Pipeline (Phases 2 & 3)**:
   ```bash
   python scripts/process_and_visualize.py
   ```

4. **Verify SQL Database Schema & Queries (Phase 4)**:
   ```bash
   python scripts/test_sql_queries.py
   ```

5. **Generate Jupyter Notebook (Phase 2)**:
   ```bash
   python scripts/build_notebook.py
   ```

6. **Open Notebook**:
   ```bash
   jupyter notebook notebooks/marketing_analysis.ipynb
   ```
