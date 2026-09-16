-- =============================================================================
-- MARKETING ANALYTICS - ADVANCED SQL QUERIES
-- Features: CTEs, Window Functions (RANK, LAG, SUM OVER), and CASE Expressions
-- =============================================================================

-- -----------------------------------------------------------------------------
-- ADVANCED QUERY 1: Channel Ranking by Revenue & ROI using Window Functions
-- Ranks each marketing channel based on Revenue and ROI independently.
-- -----------------------------------------------------------------------------
WITH ChannelStats AS (
    SELECT 
        c.Channel,
        SUM(f.Marketing_Spend) AS Total_Spend,
        SUM(f.Revenue) AS Total_Revenue,
        SUM(f.Conversions) AS Total_Conversions,
        ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS ROI_Percent
    FROM fact_marketing_performance f
    JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
    GROUP BY c.Channel
)
SELECT 
    Channel,
    Total_Spend,
    Total_Revenue,
    ROI_Percent,
    RANK() OVER (ORDER BY Total_Revenue DESC) AS Revenue_Rank,
    RANK() OVER (ORDER BY ROI_Percent DESC) AS ROI_Rank,
    DENSE_RANK() OVER (ORDER BY Total_Conversions DESC) AS Conversion_Rank
FROM ChannelStats
ORDER BY Revenue_Rank ASC;

-- -----------------------------------------------------------------------------
-- ADVANCED QUERY 2: Month-over-Month (MoM) Revenue Growth Rate using LAG()
-- Calculates monthly revenue, previous month revenue, and percentage growth.
-- -----------------------------------------------------------------------------
WITH MonthlyRevenue AS (
    SELECT 
        SUBSTR(c.Campaign_Date, 1, 7) AS Month,
        SUM(f.Revenue) AS Current_Month_Revenue,
        SUM(f.Marketing_Spend) AS Current_Month_Spend
    FROM fact_marketing_performance f
    JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
    GROUP BY SUBSTR(c.Campaign_Date, 1, 7)
),
MoM_Analysis AS (
    SELECT 
        Month,
        Current_Month_Revenue,
        Current_Month_Spend,
        LAG(Current_Month_Revenue, 1) OVER (ORDER BY Month) AS Previous_Month_Revenue
    FROM MonthlyRevenue
)
SELECT 
    Month,
    Current_Month_Revenue,
    Previous_Month_Revenue,
    ROUND(
        CASE 
            WHEN Previous_Month_Revenue IS NULL THEN 0.0
            ELSE ((Current_Month_Revenue - Previous_Month_Revenue) * 100.0 / Previous_Month_Revenue)
        END, 2
    ) AS MoM_Growth_Percent
FROM MoM_Analysis
ORDER BY Month ASC;

-- -----------------------------------------------------------------------------
-- ADVANCED QUERY 3: Campaign Performance Tiering & Classification using CASE
-- Categorizes campaigns into High ROI, Moderate ROI, Break-Even, or Loss Making.
-- -----------------------------------------------------------------------------
WITH CampaignROI AS (
    SELECT 
        c.Campaign_ID,
        c.Campaign_Name,
        c.Channel,
        SUM(f.Marketing_Spend) AS Spend,
        SUM(f.Revenue) AS Revenue,
        ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS ROI_Percent
    FROM fact_marketing_performance f
    JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
    GROUP BY c.Campaign_ID, c.Campaign_Name, c.Channel
)
SELECT 
    Campaign_ID,
    Campaign_Name,
    Channel,
    Spend,
    Revenue,
    ROI_Percent,
    CASE 
        WHEN ROI_Percent >= 100.0 THEN 'Tier 1: Exceptional (100%+ ROI)'
        WHEN ROI_Percent BETWEEN 30.0 AND 99.99 THEN 'Tier 2: Strong (30%-100% ROI)'
        WHEN ROI_Percent BETWEEN 0.0 AND 29.99 THEN 'Tier 3: Moderate (0%-30% ROI)'
        ELSE 'Tier 4: Underperforming (Negative ROI)'
    END AS Performance_Tier
FROM CampaignROI
ORDER BY ROI_Percent DESC;

-- -----------------------------------------------------------------------------
-- ADVANCED QUERY 4: Cumulative Revenue Contribution & Percentage Share
-- Uses SUM() OVER () window function to calculate running total and total share.
-- -----------------------------------------------------------------------------
WITH ChannelTotals AS (
    SELECT 
        c.Channel,
        SUM(f.Revenue) AS Channel_Revenue
    FROM fact_marketing_performance f
    JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
    GROUP BY c.Channel
)
SELECT 
    Channel,
    Channel_Revenue,
    SUM(Channel_Revenue) OVER () AS Grand_Total_Revenue,
    ROUND((Channel_Revenue * 100.0 / SUM(Channel_Revenue) OVER ()), 2) AS Revenue_Share_Percent,
    ROUND(SUM(Channel_Revenue) OVER (ORDER BY Channel_Revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS Cumulative_Revenue
FROM ChannelTotals
ORDER BY Channel_Revenue DESC;
