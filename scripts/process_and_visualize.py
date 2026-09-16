"""
Data Cleaning, Feature Engineering, KPI Calculation, Visualization, and SQL Table Export Pipeline
for Marketing Analytics Project.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 150

def run_pipeline(show_plots=False):
    raw_path = os.path.join('data', 'raw', 'marketing_data_raw.csv')
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run generate_dataset.py first.")
        
    print(f"--- 1. LOADING RAW DATASET ---")
    df = pd.read_csv(raw_path)
    initial_shape = df.shape
    print(f"Raw Data Shape: {initial_shape[0]} rows, {initial_shape[1]} columns")
    
    # ---------------------------------------------------------
    # 2. DATA CLEANING
    # ---------------------------------------------------------
    print("\n--- 2. EXECUTING DATA CLEANING ---")
    
    # A. Remove Duplicates
    num_dups = df.duplicated().sum()
    print(f"Duplicate rows detected: {num_dups}")
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Shape after duplicate removal: {df.shape}")
    
    # B. Clean Categorical Values (Strings)
    df['Channel'] = df['Channel'].astype(str).str.strip().str.title()
    channel_mapping = {
        'Google Ads': 'Google Ads',
        'Google ads': 'Google Ads',
        'Facebook': 'Facebook',
        'Instagram': 'Instagram',
        'Youtube': 'YouTube',
        'Email': 'Email',
        'Search': 'Search',
        'Display': 'Display',
        'Referral': 'Referral'
    }
    df['Channel'] = df['Channel'].replace(channel_mapping)
    
    # Standardize string fields
    df['Customer_Segment'] = df['Customer_Segment'].fillna('Unknown').astype(str).str.strip()
    df['Campaign_Type'] = df['Campaign_Type'].astype(str).str.strip()
    df['Product_Category'] = df['Product_Category'].astype(str).str.strip()
    df['City'] = df['City'].astype(str).str.strip()
    df['Region'] = df['Region'].astype(str).str.strip()
    
    # C. Datetime Conversion
    df['Campaign_Date'] = pd.to_datetime(df['Campaign_Date'])
    df['Year_Month'] = df['Campaign_Date'].dt.to_period('M').astype(str)
    
    # D. Missing Value Imputation
    print("Imputing missing values...")
    missing_leads = df['Leads'].isna().sum()
    print(f"Missing Leads: {missing_leads}")
    df['Leads'] = df['Leads'].fillna(df['Clicks'] * 0.15).astype(int)
    
    missing_rev = df['Revenue'].isna().sum()
    print(f"Missing Revenue: {missing_rev}")
    df['Revenue'] = df.apply(
        lambda r: round(r['Conversions'] * r['Order_Value'], 2) if pd.isna(r['Revenue']) else r['Revenue'],
        axis=1
    )
    
    mode_segment = df[df['Customer_Segment'] != 'Unknown']['Customer_Segment'].mode()[0]
    df['Customer_Segment'] = df['Customer_Segment'].replace('Unknown', mode_segment)
    
    # E. Outlier Handling (Cap extreme spend & revenue at 99.5th percentile for clean analytics)
    spend_cap = df['Marketing_Spend'].quantile(0.995)
    rev_cap = df['Revenue'].quantile(0.995)
    
    df['Marketing_Spend'] = np.where(df['Marketing_Spend'] > spend_cap, spend_cap, df['Marketing_Spend'])
    df['Revenue'] = np.where(df['Revenue'] > rev_cap, rev_cap, df['Revenue'])
    
    # ---------------------------------------------------------
    # 3. FEATURE ENGINEERING
    # ---------------------------------------------------------
    print("\n--- 3. FEATURE ENGINEERING & KPI METRICS ---")
    
    df['CTR'] = np.where(df['Impressions'] > 0, (df['Clicks'] / df['Impressions']) * 100, 0.0)
    df['Conversion_Rate'] = np.where(df['Leads'] > 0, (df['Conversions'] / df['Leads']) * 100, 0.0)
    df['Cost_Per_Click'] = np.where(df['Clicks'] > 0, df['Marketing_Spend'] / df['Clicks'], 0.0)
    df['Cost_Per_Lead'] = np.where(df['Leads'] > 0, df['Marketing_Spend'] / df['Leads'], 0.0)
    df['Cost_Per_Acquisition'] = np.where(df['Conversions'] > 0, df['Marketing_Spend'] / df['Conversions'], 0.0)
    df['Revenue_Per_Conversion'] = np.where(df['Conversions'] > 0, df['Revenue'] / df['Conversions'], 0.0)
    df['ROI'] = np.where(df['Marketing_Spend'] > 0, ((df['Revenue'] - df['Marketing_Spend']) / df['Marketing_Spend']) * 100, 0.0)
    
    age_bins = [17, 25, 35, 50, 65, 100]
    age_labels = ['18-25', '26-35', '36-50', '51-65', '65+']
    df['Age_Group'] = pd.cut(df['Customer_Age'], bins=age_bins, labels=age_labels)
    
    # Save Clean Processed Data
    proc_dir = os.path.join('data', 'processed')
    os.makedirs(proc_dir, exist_ok=True)
    
    clean_csv_path = os.path.join(proc_dir, 'marketing_data_clean.csv')
    df.to_csv(clean_csv_path, index=False)
    print(f"Cleaned master dataset saved to: {clean_csv_path}")

    # Export Relational Dimension & Fact Tables for SQL / Power BI
    dim_customers = df[['Customer_ID', 'Customer_Age', 'Age_Group', 'Gender', 'City', 'Region', 'Customer_Segment']].drop_duplicates(subset=['Customer_ID'])
    dim_customers.to_csv(os.path.join(proc_dir, 'dim_customers.csv'), index=False)
    
    dim_campaigns = df[['Campaign_ID', 'Campaign_Name', 'Campaign_Date', 'Channel', 'Campaign_Type']].drop_duplicates(subset=['Campaign_ID'])
    dim_campaigns.to_csv(os.path.join(proc_dir, 'dim_campaigns.csv'), index=False)
    
    prod_map = {name: f"PRD-{idx+1:02d}" for idx, name in enumerate(df['Product'].unique())}
    df['Product_ID'] = df['Product'].map(prod_map)
    dim_products = df[['Product_ID', 'Product', 'Product_Category', 'Order_Value']].drop_duplicates(subset=['Product_ID'])
    dim_products.to_csv(os.path.join(proc_dir, 'dim_products.csv'), index=False)
    
    df['Record_ID'] = np.arange(1, len(df) + 1)
    fact_performance = df[['Record_ID', 'Customer_ID', 'Campaign_ID', 'Product_ID', 'Impressions', 'Clicks', 'Leads', 'Conversions', 'Marketing_Spend', 'Revenue', 'CTR', 'Conversion_Rate', 'Cost_Per_Acquisition', 'ROI']]
    fact_performance.to_csv(os.path.join(proc_dir, 'fact_marketing_performance.csv'), index=False)
    
    print("Relational Star Schema tables exported successfully!")

    # ---------------------------------------------------------
    # 4. KPI SUMMARY CALCULATION
    # ---------------------------------------------------------
    tot_spend = df['Marketing_Spend'].sum()
    tot_rev = df['Revenue'].sum()
    tot_imp = df['Impressions'].sum()
    tot_clicks = df['Clicks'].sum()
    tot_leads = df['Leads'].sum()
    tot_conv = df['Conversions'].sum()
    
    overall_ctr = (tot_clicks / tot_imp) * 100
    overall_conv_rate = (tot_conv / tot_leads) * 100
    overall_roi = ((tot_rev - tot_spend) / tot_spend) * 100
    overall_cpa = tot_spend / tot_conv
    
    print("\n==========================================")
    print("          OVERALL MARKETING KPIS          ")
    print("==========================================")
    print(f"Total Marketing Spend:  ${tot_spend:,.2f}")
    print(f"Total Revenue Generated:${tot_rev:,.2f}")
    print(f"Total Net Profit:       ${(tot_rev - tot_spend):,.2f}")
    print(f"Total Impressions:      {tot_imp:,}")
    print(f"Total Clicks:           {tot_clicks:,}")
    print(f"Total Leads:            {tot_leads:,}")
    print(f"Total Conversions:      {tot_conv:,}")
    print(f"Overall CTR:            {overall_ctr:.2f}%")
    print(f"Overall Conversion Rate:{overall_conv_rate:.2f}%")
    print(f"Overall ROI:            {overall_roi:.2f}%")
    print(f"Blended CPA:            ${overall_cpa:.2f}")
    print("==========================================\n")

    # ---------------------------------------------------------
    # 5. GENERATE HIGH-QUALITY VISUALIZATIONS
    # ---------------------------------------------------------
    viz_dir = 'visualizations'
    os.makedirs(viz_dir, exist_ok=True)
    print("Generating 14 professional charts...")
    
    def save_and_maybe_show(filename):
        path = os.path.join(viz_dir, filename)
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        if show_plots:
            plt.show()
        plt.close()

    # 1. Monthly Revenue Trend
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly = df.groupby('Year_Month')[['Revenue', 'Marketing_Spend']].sum().reset_index()
    sns.lineplot(data=monthly, x='Year_Month', y='Revenue', marker='o', color='#2ecc71', linewidth=2.5, label='Revenue ($)', ax=ax)
    sns.lineplot(data=monthly, x='Year_Month', y='Marketing_Spend', marker='s', color='#e74c3c', linewidth=2.5, linestyle='--', label='Spend ($)', ax=ax)
    ax.set_title('Monthly Revenue vs Marketing Spend (2024 - 2025)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Year-Month', fontsize=11)
    ax.set_ylabel('Amount ($)', fontsize=11)
    plt.xticks(rotation=45)
    save_and_maybe_show('01_monthly_revenue_trend.png')
    
    # 2. Monthly Marketing Spend Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=monthly, x='Year_Month', y='Marketing_Spend', hue='Year_Month', palette='Blues_d', legend=False, ax=ax)
    ax.set_title('Monthly Marketing Spend Breakdown', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Year-Month', fontsize=11)
    ax.set_ylabel('Total Spend ($)', fontsize=11)
    plt.xticks(rotation=45)
    save_and_maybe_show('02_monthly_marketing_spend.png')

    # 3. Revenue by Channel
    fig, ax = plt.subplots(figsize=(9, 5))
    chan_perf = df.groupby('Channel')[['Revenue', 'Marketing_Spend', 'Conversions']].sum().reset_index()
    chan_perf['ROI'] = ((chan_perf['Revenue'] - chan_perf['Marketing_Spend']) / chan_perf['Marketing_Spend']) * 100
    chan_perf = chan_perf.sort_values(by='Revenue', ascending=False)
    
    sns.barplot(data=chan_perf, x='Revenue', y='Channel', hue='Channel', palette='viridis', legend=False, ax=ax)
    ax.set_title('Total Revenue Generated by Marketing Channel', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Revenue ($)', fontsize=11)
    ax.set_ylabel('Channel', fontsize=11)
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'${width:,.0f}', (width * 0.85, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    save_and_maybe_show('03_revenue_by_channel.png')

    # 4. Marketing Spend by Channel
    fig, ax = plt.subplots(figsize=(9, 5))
    chan_spend = chan_perf.sort_values(by='Marketing_Spend', ascending=False)
    sns.barplot(data=chan_spend, x='Marketing_Spend', y='Channel', hue='Channel', palette='rocket', legend=False, ax=ax)
    ax.set_title('Total Marketing Spend by Channel', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Marketing Spend ($)', fontsize=11)
    ax.set_ylabel('Channel', fontsize=11)
    save_and_maybe_show('04_marketing_spend_by_channel.png')

    # 5. Conversions by Channel
    fig, ax = plt.subplots(figsize=(9, 5))
    chan_conv = chan_perf.sort_values(by='Conversions', ascending=False)
    sns.barplot(data=chan_conv, x='Conversions', y='Channel', hue='Channel', palette='magma', legend=False, ax=ax)
    ax.set_title('Total Conversions by Marketing Channel', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Total Conversions', fontsize=11)
    ax.set_ylabel('Channel', fontsize=11)
    save_and_maybe_show('05_conversions_by_channel.png')

    # 6. ROI by Channel
    fig, ax = plt.subplots(figsize=(9, 5))
    chan_roi = chan_perf.sort_values(by='ROI', ascending=False)
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in chan_roi['ROI']]
    sns.barplot(data=chan_roi, x='ROI', y='Channel', hue='Channel', palette=colors, legend=False, ax=ax)
    ax.set_title('Return on Investment (ROI %) by Marketing Channel', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('ROI (%)', fontsize=11)
    ax.set_ylabel('Channel', fontsize=11)
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{width:.1f}%', (width + 5 if width >= 0 else width - 15, p.get_y() + p.get_height() / 2.),
                    ha='left' if width >= 0 else 'right', va='center', fontweight='bold', fontsize=9)
    save_and_maybe_show('06_roi_by_channel.png')

    # 7. Top Campaigns by Revenue
    fig, ax = plt.subplots(figsize=(10, 5))
    cmp_perf = df.groupby(['Campaign_Name', 'Campaign_ID'])[['Revenue', 'Marketing_Spend', 'Conversions']].sum().reset_index()
    cmp_perf['ROI'] = ((cmp_perf['Revenue'] - cmp_perf['Marketing_Spend']) / cmp_perf['Marketing_Spend']) * 100
    top_cmp_rev = cmp_perf.sort_values(by='Revenue', ascending=False).head(8)
    
    sns.barplot(data=top_cmp_rev, x='Revenue', y='Campaign_Name', hue='Campaign_Name', palette='crest', legend=False, ax=ax)
    ax.set_title('Top Campaigns by Total Revenue Generated', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Revenue ($)', fontsize=11)
    ax.set_ylabel('Campaign Name', fontsize=11)
    save_and_maybe_show('07_top_campaigns_by_revenue.png')

    # 8. Top Campaigns by ROI
    fig, ax = plt.subplots(figsize=(10, 5))
    top_cmp_roi = cmp_perf.sort_values(by='ROI', ascending=False).head(8)
    sns.barplot(data=top_cmp_roi, x='ROI', y='Campaign_Name', hue='Campaign_Name', palette='Spectral', legend=False, ax=ax)
    ax.set_title('Top Campaigns by ROI (%)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('ROI (%)', fontsize=11)
    ax.set_ylabel('Campaign Name', fontsize=11)
    save_and_maybe_show('08_top_campaigns_by_roi.png')

    # 9. Customer Segment Revenue
    fig, ax = plt.subplots(figsize=(8, 5))
    seg_rev = df.groupby('Customer_Segment')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    sns.barplot(data=seg_rev, x='Customer_Segment', y='Revenue', hue='Customer_Segment', palette='Set2', legend=False, ax=ax)
    ax.set_title('Revenue Breakdown by Customer Segment', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Customer Segment', fontsize=11)
    ax.set_ylabel('Revenue ($)', fontsize=11)
    save_and_maybe_show('09_customer_segment_revenue.png')

    # 10. Product Category Revenue
    fig, ax = plt.subplots(figsize=(8, 5))
    prod_rev = df.groupby('Product_Category')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    sns.barplot(data=prod_rev, x='Product_Category', y='Revenue', hue='Product_Category', palette='Dark2', legend=False, ax=ax)
    ax.set_title('Revenue Generated by Product Category', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Product Category', fontsize=11)
    ax.set_ylabel('Revenue ($)', fontsize=11)
    save_and_maybe_show('10_product_category_revenue.png')

    # 11. Age Group Conversion Rate
    fig, ax = plt.subplots(figsize=(8, 5))
    age_conv = df.groupby('Age_Group', observed=False)[['Conversions', 'Leads']].sum().reset_index()
    age_conv['Conv_Rate'] = (age_conv['Conversions'] / age_conv['Leads']) * 100
    sns.barplot(data=age_conv, x='Age_Group', y='Conv_Rate', hue='Age_Group', palette='Purples_d', legend=False, ax=ax)
    ax.set_title('Conversion Rate (%) Across Customer Age Groups', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Age Group', fontsize=11)
    ax.set_ylabel('Conversion Rate (%)', fontsize=11)
    save_and_maybe_show('11_age_group_conversion_rate.png')

    # 12. Spend vs Revenue Scatter Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='Marketing_Spend', y='Revenue', hue='Channel', alpha=0.6, s=50, ax=ax)
    ax.set_title('Marketing Spend vs. Revenue Generated Scatter', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Marketing Spend ($)', fontsize=11)
    ax.set_ylabel('Revenue ($)', fontsize=11)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    save_and_maybe_show('12_spend_vs_revenue.png')

    # 13. Clicks vs Conversions
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='Clicks', y='Conversions', hue='Campaign_Type', alpha=0.6, s=50, ax=ax)
    ax.set_title('Clicks vs. Conversions Correlation', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Clicks', fontsize=11)
    ax.set_ylabel('Conversions', fontsize=11)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    save_and_maybe_show('13_clicks_vs_conversions.png')

    # 14. Marketing Funnel Horizontal Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    funnel_stages = ['Impressions', 'Clicks', 'Leads', 'Conversions']
    funnel_values = [tot_imp, tot_clicks, tot_leads, tot_conv]
    funnel_df = pd.DataFrame({'Stage': funnel_stages, 'Volume': funnel_values})
    
    sns.barplot(data=funnel_df, x='Volume', y='Stage', hue='Stage', palette='cividis', legend=False, ax=ax)
    ax.set_title('Overall Marketing Conversion Funnel Volume', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Volume (Log Scale for Visibility)', fontsize=11)
    ax.set_xscale('log')
    for p in ax.patches:
        width = p.get_width()
        if width > 0:
            # Calculate logarithmic midpoint for perfect annotation placement
            log_mid = 10 ** (np.log10(width) / 2)
            ax.annotate(f'{int(width):,}', (log_mid, p.get_y() + p.get_height() / 2.),
                        ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    save_and_maybe_show('14_marketing_funnel.png')

    print("All 14 visualizations generated and saved to visualizations/ directory successfully!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Marketing Analytics Data Pipeline.")
    parser.add_argument('--no-show', action='store_true', help="Disable interactive pop-up chart windows during execution.")
    args = parser.parse_args()
    
    # Default show_plots to True so running the script displays pop-up windows directly
    run_pipeline(show_plots=not args.no_show)
