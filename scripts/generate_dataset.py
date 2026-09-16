"""
Synthetic Dataset Generator for Marketing Analytics Portfolio Project

Creates a realistic dataset containing ~12,000 rows with statistical relationships between:
- Spend -> Impressions -> Clicks -> Leads -> Conversions -> Revenue
- Channel performance variations
- Seasonal trends across 2024 - 2025
- Customer demographics & product categories
- Injected data quality issues (missing values, duplicates, formatting flaws, outliers)

DISCLAIMER: This dataset consists purely of SIMULATED/SYNTHETIC DATA for educational and portfolio demonstration purposes.
"""

import os
import random
import numpy as np
import pandas as pd

def generate_marketing_dataset(num_records=12500, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    # -------------------------------------------------------------
    # 1. Dimension Lists & Base Probability Weightings
    # -------------------------------------------------------------
    channels = ['Google Ads', 'Facebook', 'Instagram', 'YouTube', 'Email', 'Search', 'Display', 'Referral']
    channel_weights = [0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05, 0.05]
    
    # Base Channel CTR & Conversion Multipliers
    channel_props = {
        'Google Ads':   {'base_ctr': 0.045, 'conv_mult': 1.25, 'cpc_base': 2.50},
        'Search':       {'base_ctr': 0.052, 'conv_mult': 1.35, 'cpc_base': 2.10},
        'Email':        {'base_ctr': 0.060, 'conv_mult': 1.40, 'cpc_base': 0.40},
        'Facebook':     {'base_ctr': 0.028, 'conv_mult': 0.95, 'cpc_base': 1.80},
        'Instagram':    {'base_ctr': 0.032, 'conv_mult': 1.05, 'cpc_base': 1.95},
        'YouTube':      {'base_ctr': 0.018, 'conv_mult': 0.85, 'cpc_base': 2.20},
        'Referral':     {'base_ctr': 0.048, 'conv_mult': 1.50, 'cpc_base': 1.10},
        'Display':      {'base_ctr': 0.012, 'conv_mult': 0.55, 'cpc_base': 1.20}
    }
    
    campaign_types = ['Brand Awareness', 'Lead Generation', 'Retargeting', 'Seasonal Sale', 'Product Launch']
    
    campaign_templates = [
        ('CMP-101', 'Q1 Brand Refresh', 'Brand Awareness'),
        ('CMP-102', 'Spring Tech Blowout', 'Seasonal Sale'),
        ('CMP-103', 'Enterprise SaaS LeadGen', 'Lead Generation'),
        ('CMP-104', 'Summer Fashion Retargeting', 'Retargeting'),
        ('CMP-105', 'SmartHome Hub Launch', 'Product Launch'),
        ('CMP-106', 'Fall Hardware Promo', 'Seasonal Sale'),
        ('CMP-107', 'Cyber November Mega Sale', 'Seasonal Sale'),
        ('CMP-108', 'Holiday Gift Extravaganza', 'Seasonal Sale'),
        ('CMP-109', 'Email Newsletter Nurture', 'Lead Generation'),
        ('CMP-110', 'Display Banner Remarketing', 'Retargeting'),
        ('CMP-111', 'Influencer Video Push', 'Brand Awareness'),
        ('CMP-112', 'VIP Customer Loyalty Drive', 'Retargeting'),
        ('CMP-113', 'High-Spend Experimental Push', 'Brand Awareness'), # Intentional low ROI campaign
        ('CMP-114', 'Low-Budget High-Conversion Niche', 'Lead Generation') # Intentional high ROI campaign
    ]
    
    product_catalog = [
        {'id': 'PRD-01', 'name': 'CloudAnalytics Pro SaaS', 'category': 'Software/SaaS', 'base_price': 499.0},
        {'id': 'PRD-02', 'name': 'Smart noise-canceling Headphones', 'category': 'Electronics', 'base_price': 199.0},
        {'id': 'PRD-03', 'name': 'Ergonomic Executive Chair', 'category': 'Home & Living', 'base_price': 299.0},
        {'id': 'PRD-04', 'name': 'UltraFit Smartwatch 5', 'category': 'Fitness', 'base_price': 149.0},
        {'id': 'PRD-05', 'name': 'Premium Designer Denim Jacket', 'category': 'Apparel', 'base_price': 89.0},
        {'id': 'PRD-06', 'name': 'CyberSecurity Enterprise Suite', 'category': 'Software/SaaS', 'base_price': 1200.0},
        {'id': 'PRD-07', 'name': '4K UltraHD Streamer Box', 'category': 'Electronics', 'base_price': 129.0},
        {'id': 'PRD-08', 'name': 'Adjustable Standing Desk', 'category': 'Home & Living', 'base_price': 450.0}
    ]
    
    cities_regions = [
        ('New York', 'North East'),
        ('Boston', 'North East'),
        ('Philadelphia', 'North East'),
        ('Chicago', 'Midwest'),
        ('Detroit', 'Midwest'),
        ('Minneapolis', 'Midwest'),
        ('Atlanta', 'South'),
        ('Dallas', 'South'),
        ('Miami', 'South'),
        ('Los Angeles', 'West'),
        ('San Francisco', 'West'),
        ('Seattle', 'West')
    ]
    
    customer_segments = ['B2B Enterprise', 'SMB', 'Consumer Premium', 'Consumer Budget']
    
    genders = ['Male', 'Female', 'Non-Binary', 'Other']

    # -------------------------------------------------------------
    # 2. Date Range Generation (2024-01-01 to 2025-06-30)
    # -------------------------------------------------------------
    start_date = pd.Timestamp('2024-01-01')
    end_date = pd.Timestamp('2025-06-30')
    total_days = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        # Customer ID
        cust_id_num = np.random.randint(1000, 9999)
        cust_id = f"CUST-{cust_id_num}"
        
        # Demographics
        cust_age = int(np.random.normal(loc=38, scale=12))
        cust_age = max(18, min(75, cust_age))
        
        gender = np.random.choice(genders, p=[0.47, 0.47, 0.04, 0.02])
        city, region = random.choice(cities_regions)
        cust_segment = np.random.choice(customer_segments, p=[0.15, 0.30, 0.25, 0.30])
        
        # Date & Seasonality
        random_day = random.randint(0, total_days)
        record_date = start_date + pd.Timedelta(days=random_day)
        month = record_date.month
        
        # Seasonal multiplier (November/December boost, Summer mid-boost, Jan slump)
        if month in [11, 12]:
            season_mult = 1.45
        elif month in [6, 7]:
            season_mult = 1.15
        elif month == 1:
            season_mult = 0.80
        else:
            season_mult = 1.00
            
        # Campaign selection
        cmp_id, cmp_name, cmp_type = random.choice(campaign_templates)
        
        # Channel selection
        channel = np.random.choice(channels, p=channel_weights)
        c_info = channel_props[channel]
        
        # Product selection based on segment
        if cust_segment == 'B2B Enterprise':
            prod = product_catalog[0] if random.random() < 0.6 else product_catalog[5]
        elif cust_segment == 'SMB':
            prod = random.choice([product_catalog[0], product_catalog[2], product_catalog[7]])
        elif cust_segment == 'Consumer Premium':
            prod = random.choice([product_catalog[1], product_catalog[2], product_catalog[3], product_catalog[7]])
        else:
            prod = random.choice([product_catalog[3], product_catalog[4], product_catalog[6]])
            
        # Financial & Performance Calculations
        base_spend = np.random.uniform(100, 2500)
        
        # Low-spend/high-spend anomalies by campaign
        if cmp_id == 'CMP-113': # High spend, low return
            base_spend *= 3.5
        elif cmp_id == 'CMP-114': # Low spend, high return
            base_spend *= 0.5
            
        spend = round(base_spend * season_mult, 2)
        
        # Impressions
        cost_per_thousand = np.random.uniform(8.0, 25.0)
        impressions = int((spend / cost_per_thousand) * 1000)
        impressions = max(500, impressions)
        
        # Clicks
        ctr = c_info['base_ctr'] * np.random.uniform(0.8, 1.2)
        clicks = int(impressions * ctr)
        clicks = max(10, clicks)
        
        # Leads
        lead_rate = 0.20 if cmp_type == 'Lead Generation' else 0.10
        leads = int(clicks * lead_rate * np.random.uniform(0.7, 1.3))
        leads = min(clicks, max(1, leads))
        
        # Conversions
        base_conv_rate = 0.12 * c_info['conv_mult']
        if cmp_id == 'CMP-113':
            base_conv_rate *= 0.25 # Underperforming campaign
        elif cmp_id == 'CMP-114':
            base_conv_rate *= 2.2 # Top performing campaign
            
        conversions = int(leads * base_conv_rate * np.random.uniform(0.8, 1.2))
        conversions = min(leads, max(0, conversions))
        
        # Revenue & Order Value
        order_value = round(prod['base_price'] * np.random.uniform(0.9, 1.1), 2)
        revenue = round(conversions * order_value, 2)
        
        # Customer Acquisition Cost
        cac = round(spend / conversions, 2) if conversions > 0 else 0.0
        
        records.append({
            'Customer_ID': cust_id,
            'Customer_Age': cust_age,
            'Gender': gender,
            'City': city,
            'Region': region,
            'Customer_Segment': cust_segment,
            'Campaign_ID': cmp_id,
            'Campaign_Name': cmp_name,
            'Campaign_Date': record_date.strftime('%Y-%m-%d'),
            'Channel': channel,
            'Campaign_Type': cmp_type,
            'Product_Category': prod['category'],
            'Product': prod['name'],
            'Impressions': impressions,
            'Clicks': clicks,
            'Leads': leads,
            'Conversions': conversions,
            'Marketing_Spend': spend,
            'Revenue': revenue,
            'Customer_Acquisition_Cost': cac,
            'Order_Value': order_value
        })
        
    df = pd.DataFrame(records)
    
    # -------------------------------------------------------------
    # 3. Inject Data Quality Issues for Cleaning Demonstration
    # -------------------------------------------------------------
    print("Injecting realistic data quality issues...")
    
    # A. Introduce Missing Values (~3% in selected columns)
    null_idx_leads = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df.loc[null_idx_leads, 'Leads'] = np.nan
    
    null_idx_rev = np.random.choice(df.index, size=int(len(df) * 0.025), replace=False)
    df.loc[null_idx_rev, 'Revenue'] = np.nan

    null_idx_seg = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
    df.loc[null_idx_seg, 'Customer_Segment'] = np.nan

    # B. Introduce Categorical Casing & Whitespace Anomalies
    channel_anomalies = {
        'Google Ads': ['google ads', 'Google Ads  ', 'GOOGLE ADS'],
        'Facebook': ['facebook', 'Facebook  ', 'FACEBOOK'],
        'Email': ['email', 'Email  '],
        'Instagram': ['instagram', 'Instagram ']
    }
    
    for real_chan, bad_chans in channel_anomalies.items():
        sample_idx = df[df['Channel'] == real_chan].sample(frac=0.08, random_state=42).index
        df.loc[sample_idx, 'Channel'] = np.random.choice(bad_chans, size=len(sample_idx))
        
    # C. Introduce Outliers (Extreme Spend / Revenue)
    outlier_idx_spend = np.random.choice(df.index, size=15, replace=False)
    df.loc[outlier_idx_spend, 'Marketing_Spend'] = df.loc[outlier_idx_spend, 'Marketing_Spend'] * 15.0
    
    outlier_idx_rev = np.random.choice(df.index, size=10, replace=False)
    df.loc[outlier_idx_rev, 'Revenue'] = df.loc[outlier_idx_rev, 'Revenue'] * 12.0

    # D. Inject Duplicate Records (~2%)
    dup_rows = df.sample(n=int(len(df) * 0.02), random_state=42)
    df = pd.concat([df, dup_rows], ignore_index=True)
    
    # Shuffle dataframe
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    return df

if __name__ == '__main__':
    raw_dir = os.path.join('data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    print("Generating synthetic marketing dataset...")
    marketing_df = generate_marketing_dataset(num_records=12000, seed=42)
    
    output_path = os.path.join(raw_dir, 'marketing_data_raw.csv')
    marketing_df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully! Total rows: {len(marketing_df)}")
    print(f"Saved to: {os.path.abspath(output_path)}")
