# Power BI Marketing Analytics Dashboard Specification

## Overview & Architecture
This document details the architectural blueprint and design specification for constructing a publication-grade, 4-page Power BI dashboard. The data model utilizes a Star Schema connecting `fact_marketing_performance` to `dim_customers`, `dim_campaigns`, and `dim_products`.

---

## Data Model & Relationships

```
           +--------------------+
           |   dim_customers    |
           +--------------------+
           | Customer_ID (PK)   |
           +---------+----------:
                     | (1:N)
                     v
+--------------------+--------------------+
|            fact_marketing_performance   |
+-----------------------------------------+
| Record_ID (PK)                          |
| Customer_ID (FK)                        |
| Campaign_ID (FK)                        |
| Product_ID (FK)                         |
| Impressions, Clicks, Leads, Conversions |
| Spend, Revenue, CTR, Conv_Rate, CPA, ROI|
+--------------------+--------------------+
                     ^                   ^
               (N:1) |                   | (N:1)
           +---------+----------+  +-----+--------------+
           |    dim_campaigns   |  |     dim_products   |
           +--------------------+  +--------------------+
           | Campaign_ID (PK)   |  | Product_ID (PK)    |
           +--------------------+  +--------------------+
```

---

## Design System & Theme Settings

- **Color Palette**:
  - Primary Theme: Dark Slate / Navy (#1e293b)
  - Accent Green (Revenue / ROI): #10b981
  - Accent Blue (Spend / Impressions): #3b82f6
  - Accent Red (Underperforming / Costs): #ef4444
  - Neutral Background: #f8fafc
  - Card Background: #ffffff (with subtle 1px border #e2e8f0)
- **Typography**: Segoe UI / Segoe UI Semibold
- **Page Canvas Size**: 16:9 Standard Widescreen (1280 x 720 px)

---

## Page-by-Page Dashboard Layout

### PAGE 1: MARKETING OVERVIEW
**Objective**: Provide executives with an instant pulse on top-line spend, revenue, net profit, funnel conversion, and top channel drivers.

- **Header / Navigation Bar**:
  - Title: "Marketing Analytics - Executive Overview"
  - Slicers: `Date Range`, `Channel`, `Region`, `Customer Segment`

- **KPI Cards Row (Top Top-Line Metrics)**:
  1. *Total Spend*: Card showing `[Total Spend]` formatted as currency.
  2. *Total Revenue*: Card showing `[Total Revenue]` formatted as currency.
  3. *Total Conversions*: Card showing `[Total Conversions]` formatted as integer.
  4. *Overall Conversion Rate %*: Card showing `[Overall Conversion Rate %]` formatted as percentage.
  5. *Blended CPA*: Card showing `[Blended Cost Per Acquisition]` formatted as currency.
  6. *Overall ROI %*: Card showing `[Overall ROI %]` with conditional green/red formatting.

- **Visual Containers**:
  - **Visual 1 (Line & Stacked Column Chart)**: *Monthly Revenue vs Spend Trend*
    - X-Axis: `Campaign_Date` (Year-Month)
    - Y-Axis Columns: `[Total Spend]`
    - Y-Axis Line: `[Total Revenue]`
  - **Visual 2 (Horizontal Bar Chart)**: *Revenue by Marketing Channel*
    - Y-Axis: `Channel`
    - X-Axis: `[Total Revenue]`
  - **Visual 3 (Donut / Treemap Chart)**: *Spend Distribution by Channel*
    - Category: `Channel`
    - Values: `[Total Spend]`
  - **Visual 4 (Funnel Chart)**: *Marketing Conversion Funnel*
    - Stages: Impressions (100%) -> Clicks -> Leads -> Conversions

---

### PAGE 2: CAMPAIGN PERFORMANCE
**Objective**: Deep-dive into campaign-level profitability, top ROI generators vs spend-guzzlers.

- **Header Slicers**: `Campaign Type`, `Channel`, `Date Range`
- **KPI Summary**:
  - Top Campaign by Revenue: Callout Box
  - Highest ROI Campaign: Callout Box
  - Underperforming Campaigns Count: Callout Box

- **Visual Containers**:
  - **Visual 1 (Scatter Plot)**: *Marketing Spend vs Revenue by Campaign*
    - X-Axis: `[Total Spend]`
    - Y-Axis: `[Total Revenue]`
    - Size: `[Total Conversions]`
    - Legend: `Channel`
  - **Visual 2 (Clustered Bar Chart)**: *Top 10 Campaigns by Revenue*
    - Y-Axis: `Campaign_Name`
    - Values: `[Total Revenue]`, `[Total Spend]`
  - **Visual 3 (Table / Matrix)**: *Campaign ROI Performance Ledger*
    - Columns: `Campaign_Name`, `Channel`, `Spend`, `Revenue`, `Conversions`, `CPA`, `ROI %`
    - Data Bars: Applied to `ROI %` column (Green for positive, Red for negative).

---

### PAGE 3: CHANNEL ANALYSIS
**Objective**: Granular channel breakdown comparing Google Ads, Facebook, Instagram, YouTube, Email, Search, Display, and Referral.

- **Header Slicers**: `Channel`, `Region`
- **Metrics Table / Matrix Grid**:
  - Rows: `Channel`
  - Columns: `Impressions`, `Clicks`, `CTR %`, `Leads`, `Conversions`, `Conv Rate %`, `Spend`, `Revenue`, `CPA`, `ROI %`

- **Visual Containers**:
  - **Visual 1 (Clustered Column Chart)**: *Cost Per Acquisition (CPA) by Channel*
    - Category: `Channel`
    - Values: `[Blended Cost Per Acquisition]`
  - **Visual 2 (Bar Chart)**: *Return on Investment (ROI %) by Channel*
    - Category: `Channel`
    - Values: `[Overall ROI %]`
  - **Visual 3 (100% Stacked Bar Chart)**: *Channel Contribution to Conversions*
    - Legend: `Channel`
    - Values: `[Total Conversions]`

---

### PAGE 4: CUSTOMER & PRODUCT ANALYSIS
**Objective**: Analyze customer demographics, geographic performance, and product category mix.

- **Header Slicers**: `Region`, `Product Category`, `Gender`
- **Visual Containers**:
  - **Visual 1 (Bar Chart)**: *Revenue by Customer Segment*
    - Category: `Customer_Segment` (B2B Enterprise, SMB, Consumer Premium, Consumer Budget)
    - Values: `[Total Revenue]`
  - **Visual 2 (Column Chart)**: *Conversion Rate by Age Group*
    - X-Axis: `Age_Group` (18-25, 26-35, 36-50, 51-65, 65+)
    - Y-Axis: `[Overall Conversion Rate %]`
  - **Visual 3 (Map / Filled Map)**: *Regional Revenue & Spend Distribution*
    - Location: `State / City / Region`
    - Bubble Size: `[Total Revenue]`
  - **Visual 4 (Bar Chart)**: *Revenue & Units Sold by Product Category*
    - Category: `Product_Category`
    - Values: `[Total Revenue]`, `[Total Conversions]`
