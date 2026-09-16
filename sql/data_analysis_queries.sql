-- =============================================================================
-- MARKETING ANALYTICS - STANDARD ANALYTICAL QUERIES
-- Answers key business questions regarding performance, ROI, channels, and campaigns.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1: Overall Marketing KPI Summary
-- Total Spend, Total Revenue, Net Profit, Total Conversions, Overall ROI %, Blended CPA
-- -----------------------------------------------------------------------------
SELECT 
    SUM(Marketing_Spend) AS Total_Marketing_Spend,
    SUM(Revenue) AS Total_Revenue,
    SUM(Revenue) - SUM(Marketing_Spend) AS Net_Profit,
    SUM(Conversions) AS Total_Conversions,
    ROUND(((SUM(Revenue) - SUM(Marketing_Spend)) / SUM(Marketing_Spend)) * 100, 2) AS Overall_ROI_Percent,
    ROUND(SUM(Marketing_Spend) / SUM(Conversions), 2) AS Blended_CPA
FROM fact_marketing_performance;

-- -----------------------------------------------------------------------------
-- QUERY 2: Channel Performance Overview
-- Spend, Revenue, Conversions, CTR %, Conversion Rate %, CPA, and ROI % by Channel
-- -----------------------------------------------------------------------------
SELECT 
    c.Channel,
    COUNT(f.Record_ID) AS Total_Records,
    SUM(f.Marketing_Spend) AS Channel_Spend,
    SUM(f.Revenue) AS Channel_Revenue,
    SUM(f.Conversions) AS Total_Conversions,
    ROUND((SUM(f.Clicks) * 100.0 / NULLIF(SUM(f.Impressions), 0)), 2) AS CTR_Percent,
    ROUND((SUM(f.Conversions) * 100.0 / NULLIF(SUM(f.Leads), 0)), 2) AS Conv_Rate_Percent,
    ROUND(SUM(f.Marketing_Spend) / NULLIF(SUM(f.Conversions), 0), 2) AS CPA,
    ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS ROI_Percent
FROM fact_marketing_performance f
JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
GROUP BY c.Channel
ORDER BY Channel_Revenue DESC;

-- -----------------------------------------------------------------------------
-- QUERY 3: Top 10 Marketing Campaigns by Total Revenue
-- -----------------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    c.Channel,
    c.Campaign_Type,
    SUM(f.Marketing_Spend) AS Campaign_Spend,
    SUM(f.Revenue) AS Campaign_Revenue,
    SUM(f.Conversions) AS Total_Conversions,
    ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS ROI_Percent
FROM fact_marketing_performance f
JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Channel, c.Campaign_Type
ORDER BY Campaign_Revenue DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- QUERY 4: Lowest-Performing Campaigns by ROI (Underperforming Campaigns)
-- -----------------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    c.Channel,
    SUM(f.Marketing_Spend) AS Campaign_Spend,
    SUM(f.Revenue) AS Campaign_Revenue,
    ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS ROI_Percent
FROM fact_marketing_performance f
JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Channel
ORDER BY ROI_Percent ASC
LIMIT 5;

-- -----------------------------------------------------------------------------
-- QUERY 5: Revenue and Conversion Performance by Customer Segment
-- -----------------------------------------------------------------------------
SELECT 
    cust.Customer_Segment,
    COUNT(DISTINCT cust.Customer_ID) AS Total_Customers,
    SUM(f.Conversions) AS Total_Conversions,
    SUM(f.Revenue) AS Total_Revenue,
    ROUND(AVG(f.Revenue), 2) AS Avg_Revenue_Per_Record
FROM fact_marketing_performance f
JOIN dim_customers cust ON f.Customer_ID = cust.Customer_ID
GROUP BY cust.Customer_Segment
ORDER BY Total_Revenue DESC;

-- -----------------------------------------------------------------------------
-- QUERY 6: Revenue & Order Volume by Product Category
-- -----------------------------------------------------------------------------
SELECT 
    p.Product_Category,
    COUNT(DISTINCT p.Product_ID) AS Total_Products,
    SUM(f.Conversions) AS Units_Sold,
    SUM(f.Revenue) AS Category_Revenue,
    ROUND(AVG(p.Order_Value), 2) AS Avg_Order_Value
FROM fact_marketing_performance f
JOIN dim_products p ON f.Product_ID = p.Product_ID
GROUP BY p.Product_Category
ORDER BY Category_Revenue DESC;

-- -----------------------------------------------------------------------------
-- QUERY 7: Regional and City Marketing Performance
-- -----------------------------------------------------------------------------
SELECT 
    cust.Region,
    cust.City,
    COUNT(f.Record_ID) AS Records_Count,
    SUM(f.Marketing_Spend) AS Regional_Spend,
    SUM(f.Revenue) AS Regional_Revenue,
    ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS Regional_ROI
FROM fact_marketing_performance f
JOIN dim_customers cust ON f.Customer_ID = cust.Customer_ID
GROUP BY cust.Region, cust.City
ORDER BY Regional_Revenue DESC;

-- -----------------------------------------------------------------------------
-- QUERY 8: Monthly Performance Breakdown (Spend, Revenue, ROI Trend)
-- -----------------------------------------------------------------------------
SELECT 
    SUBSTR(c.Campaign_Date, 1, 7) AS Month,
    SUM(f.Marketing_Spend) AS Monthly_Spend,
    SUM(f.Revenue) AS Monthly_Revenue,
    SUM(f.Conversions) AS Monthly_Conversions,
    ROUND(((SUM(f.Revenue) - SUM(f.Marketing_Spend)) * 100.0 / NULLIF(SUM(f.Marketing_Spend), 0)), 2) AS Monthly_ROI
FROM fact_marketing_performance f
JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
GROUP BY SUBSTR(c.Campaign_Date, 1, 7)
ORDER BY Month ASC;

-- -----------------------------------------------------------------------------
-- QUERY 9: Customers Acquired by Channel
-- -----------------------------------------------------------------------------
SELECT 
    c.Channel,
    COUNT(DISTINCT f.Customer_ID) AS Unique_Customers_Acquired,
    SUM(f.Conversions) AS Total_Conversions
FROM fact_marketing_performance f
JOIN dim_campaigns c ON f.Campaign_ID = c.Campaign_ID
GROUP BY c.Channel
ORDER BY Unique_Customers_Acquired DESC;

-- -----------------------------------------------------------------------------
-- QUERY 10: Age Group Conversion Efficiency
-- -----------------------------------------------------------------------------
SELECT 
    cust.Age_Group,
    SUM(f.Leads) AS Total_Leads,
    SUM(f.Conversions) AS Total_Conversions,
    ROUND((SUM(f.Conversions) * 100.0 / NULLIF(SUM(f.Leads), 0)), 2) AS Conversion_Rate_Percent,
    SUM(f.Revenue) AS Total_Revenue
FROM fact_marketing_performance f
JOIN dim_customers cust ON f.Customer_ID = cust.Customer_ID
GROUP BY cust.Age_Group
ORDER BY Conversion_Rate_Percent DESC;
