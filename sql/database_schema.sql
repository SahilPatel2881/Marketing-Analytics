-- =============================================================================
-- MARKETING ANALYTICS DATABASE SCHEMA (DDL)
-- Database Engine Compatibility: PostgreSQL / MySQL / SQLite
-- =============================================================================

-- Drop existing tables if re-creating
DROP TABLE IF EXISTS fact_marketing_performance;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_campaigns;
DROP TABLE IF EXISTS dim_products;

-- -----------------------------------------------------------------------------
-- 1. CUSTOMERS DIMENSION TABLE (dim_customers)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_customers (
    Customer_ID VARCHAR(20) PRIMARY KEY,
    Customer_Age INT CHECK (Customer_Age >= 18),
    Age_Group VARCHAR(20),
    Gender VARCHAR(20),
    City VARCHAR(100),
    Region VARCHAR(50),
    Customer_Segment VARCHAR(50) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. CAMPAIGNS DIMENSION TABLE (dim_campaigns)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_campaigns (
    Campaign_ID VARCHAR(20) PRIMARY KEY,
    Campaign_Name VARCHAR(150) NOT NULL,
    Campaign_Date DATE NOT NULL,
    Channel VARCHAR(50) NOT NULL,
    Campaign_Type VARCHAR(50) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 3. PRODUCTS DIMENSION TABLE (dim_products)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_products (
    Product_ID VARCHAR(20) PRIMARY KEY,
    Product VARCHAR(150) NOT NULL,
    Product_Category VARCHAR(50) NOT NULL,
    Order_Value DECIMAL(10, 2) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 4. MARKETING PERFORMANCE FACT TABLE (fact_marketing_performance)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_marketing_performance (
    Record_ID INT PRIMARY KEY,
    Customer_ID VARCHAR(20) NOT NULL,
    Campaign_ID VARCHAR(20) NOT NULL,
    Product_ID VARCHAR(20) NOT NULL,
    Impressions INT NOT NULL,
    Clicks INT NOT NULL,
    Leads INT NOT NULL,
    Conversions INT NOT NULL,
    Marketing_Spend DECIMAL(10, 2) NOT NULL,
    Revenue DECIMAL(10, 2) NOT NULL,
    CTR DECIMAL(8, 4),
    Conversion_Rate DECIMAL(8, 4),
    Cost_Per_Acquisition DECIMAL(10, 2),
    ROI DECIMAL(10, 4),
    FOREIGN KEY (Customer_ID) REFERENCES dim_customers(Customer_ID),
    FOREIGN KEY (Campaign_ID) REFERENCES dim_campaigns(Campaign_ID),
    FOREIGN KEY (Product_ID) REFERENCES dim_products(Product_ID)
);

-- -----------------------------------------------------------------------------
-- INDEXES FOR QUERY OPTIMIZATION
-- -----------------------------------------------------------------------------
CREATE INDEX idx_fact_customer ON fact_marketing_performance(Customer_ID);
CREATE INDEX idx_fact_campaign ON fact_marketing_performance(Campaign_ID);
CREATE INDEX idx_fact_product ON fact_marketing_performance(Product_ID);
CREATE INDEX idx_campaign_channel ON dim_campaigns(Channel);
