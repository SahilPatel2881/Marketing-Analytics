# Data Dictionary - Marketing Analytics Dataset

> **Note**: This dataset represents **SIMULATED / SYNTHETIC DATA** created for educational, analytical, and portfolio demonstration purposes.

---

## Master Table Schema & Field Descriptions

| Column Name | Data Type | Key Type | Business Description | Value Range / Examples |
| :--- | :--- | :--- | :--- | :--- |
| `Customer_ID` | String (VARCHAR) | FK | Unique identifier assigned to each customer | `CUST-1024`, `CUST-8891` |
| `Customer_Age` | Integer (INT) | - | Age of customer in years | `18` to `75` |
| `Age_Group` | Categorical (VARCHAR) | - | Binned age bracket for demographic cohorting | `18-25`, `26-35`, `36-50`, `51-65`, `65+` |
| `Gender` | String (VARCHAR) | - | Self-identified gender of customer | `Male`, `Female`, `Non-Binary`, `Other` |
| `City` | String (VARCHAR) | - | Primary city location of customer | `New York`, `Chicago`, `Los Angeles`, `Atlanta` |
| `Region` | String (VARCHAR) | - | Geographical territory of customer | `North East`, `Midwest`, `South`, `West` |
| `Customer_Segment` | String (VARCHAR) | - | Commercial customer category | `B2B Enterprise`, `SMB`, `Consumer Premium`, `Consumer Budget` |
| `Campaign_ID` | String (VARCHAR) | FK | Unique identifier for marketing campaign | `CMP-101`, `CMP-107` |
| `Campaign_Name` | String (VARCHAR) | - | Human-readable title of marketing campaign | `Q1 Brand Refresh`, `Cyber November Mega Sale` |
| `Campaign_Date` | Date (YYYY-MM-DD) | - | Date when campaign activity / record logged | `2024-01-15` to `2025-06-30` |
| `Channel` | String (VARCHAR) | - | Digital acquisition channel | `Google Ads`, `Facebook`, `Instagram`, `Email`, `Search`, `Display`, `YouTube`, `Referral` |
| `Campaign_Type` | String (VARCHAR) | - | Strategic objective of campaign | `Brand Awareness`, `Lead Generation`, `Retargeting`, `Seasonal Sale`, `Product Launch` |
| `Product_ID` | String (VARCHAR) | FK | Unique identifier for associated product | `PRD-01` to `PRD-08` |
| `Product` | String (VARCHAR) | - | Name of product offered | `CloudAnalytics Pro SaaS`, `4K UltraHD Streamer Box` |
| `Product_Category` | String (VARCHAR) | - | High-level classification of product | `Software/SaaS`, `Electronics`, `Home & Living`, `Fitness`, `Apparel` |
| `Order_Value` | Float (DECIMAL) | - | Base price or average order value per unit | `$89.00` to `$1,200.00` |
| `Impressions` | Integer (INT) | - | Number of times marketing ad was displayed | `500` to `250,000` |
| `Clicks` | Integer (INT) | - | Number of ad clicks generated | `10` to `15,000` |
| `Leads` | Integer (INT) | - | Number of sales prospects captured | `1` to `3,000` |
| `Conversions` | Integer (INT) | - | Number of completed paid purchases | `0` to `500` |
| `Marketing_Spend` | Float (DECIMAL) | - | Total financial cost incurred for campaign | `$50.00` to `$7,500.00` |
| `Revenue` | Float (DECIMAL) | - | Gross revenue dollar amount generated | `$0.00` to `$45,000.00` |
| `CTR` | Float (DECIMAL) | Calculated | Click-Through Rate: `(Clicks / Impressions) * 100` | `0.5%` to `8.5%` |
| `Conversion_Rate` | Float (DECIMAL) | Calculated | Conversion Efficiency: `(Conversions / Leads) * 100` | `0.0%` to `35.0%` |
| `Cost_Per_Click` | Float (DECIMAL) | Calculated | CPC: `Marketing_Spend / Clicks` | `$0.20` to `$5.50` |
| `Cost_Per_Lead` | Float (DECIMAL) | Calculated | CPL: `Marketing_Spend / Leads` | `$1.50` to `$25.00` |
| `Cost_Per_Acquisition` | Float (DECIMAL) | Calculated | CPA: `Marketing_Spend / Conversions` | `$10.00` to `$350.00` |
| `Revenue_Per_Conversion`| Float (DECIMAL) | Calculated | RPC: `Revenue / Conversions` | `$89.00` to `$1,200.00` |
| `ROI` | Float (DECIMAL) | Calculated | Return on Investment: `((Revenue - Spend) / Spend) * 100` | `-100.0%` to `450.0%` |
