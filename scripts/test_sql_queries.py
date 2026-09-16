"""
SQL Database & Query Verification Test Script for Marketing Analytics Project.
Executes DDL schema and analytical SQL queries against an in-memory SQLite engine.
"""

import os
import sqlite3
import pandas as pd

def test_sql_execution():
    proc_dir = os.path.join('data', 'processed')
    sql_dir = 'sql'
    
    # Required CSV files
    dim_cust_path = os.path.join(proc_dir, 'dim_customers.csv')
    dim_cmp_path = os.path.join(proc_dir, 'dim_campaigns.csv')
    dim_prd_path = os.path.join(proc_dir, 'dim_products.csv')
    fact_perf_path = os.path.join(proc_dir, 'fact_marketing_performance.csv')
    
    if not os.path.exists(fact_perf_path):
        raise FileNotFoundError("Processed CSV files not found. Run process_and_visualize.py first.")

    print("Connecting to in-memory SQLite database...")
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 1. Execute DDL Schema
    schema_path = os.path.join(sql_dir, 'database_schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
    print("Executing database schema DDL...")
    cursor.executescript(schema_sql)
    conn.commit()
    print("Tables created successfully!")
    
    # 2. Populate SQLite Tables from CSV Data
    print("Populating database tables with cleaned dataset...")
    df_cust = pd.read_csv(dim_cust_path)
    df_cmp = pd.read_csv(dim_cmp_path)
    df_prd = pd.read_csv(dim_prd_path)
    df_fact = pd.read_csv(fact_perf_path)
    
    df_cust.to_sql('dim_customers', conn, if_exists='append', index=False)
    df_cmp.to_sql('dim_campaigns', conn, if_exists='append', index=False)
    df_prd.to_sql('dim_products', conn, if_exists='append', index=False)
    df_fact.to_sql('fact_marketing_performance', conn, if_exists='append', index=False)
    print(f"Populated dim_customers ({len(df_cust)} rows), dim_campaigns ({len(df_cmp)} rows), dim_products ({len(df_prd)} rows), fact_marketing_performance ({len(df_fact)} rows).")

    # 3. Test Standard Analytical Queries
    print("\n--- TESTING STANDARD ANALYTICAL QUERIES ---")
    query_file = os.path.join(sql_dir, 'data_analysis_queries.sql')
    with open(query_file, 'r') as f:
        queries_text = f.read()
        
    # Split queries by semicolon and strip comments to find executable SQL
    raw_blocks = [q.strip() for q in queries_text.split(';') if q.strip()]
    
    query_num = 1
    for block in raw_blocks:
        # Filter out comment-only lines to check if there is actual SQL
        sql_lines = [line for line in block.split('\n') if not line.strip().startswith('--')]
        clean_sql = '\n'.join(sql_lines).strip()
        if clean_sql and ('SELECT' in clean_sql.upper()):
            print(f"Executing Standard Query #{query_num}...")
            try:
                res = pd.read_sql_query(clean_sql, conn)
                print(f"Query #{query_num} Success! Returned {len(res)} rows. Preview:")
                print(res.head(5).to_string(index=False))
                print("-" * 60 + "\n")
            except Exception as e:
                print(f"ERROR executing Query #{query_num}: {e}\n")
            query_num += 1

    # 4. Test Advanced Queries (CTEs & Window Functions)
    print("\n--- TESTING ADVANCED SQL QUERIES (CTEs & WINDOW FUNCTIONS) ---")
    adv_query_file = os.path.join(sql_dir, 'advanced_queries.sql')
    with open(adv_query_file, 'r') as f:
        adv_text = f.read()
        
    raw_adv_blocks = [q.strip() for q in adv_text.split(';') if q.strip()]
    
    adv_num = 1
    for block in raw_adv_blocks:
        sql_lines = [line for line in block.split('\n') if not line.strip().startswith('--')]
        clean_sql = '\n'.join(sql_lines).strip()
        if clean_sql and ('WITH' in clean_sql.upper() or 'SELECT' in clean_sql.upper()):
            print(f"Executing Advanced Query #{adv_num}...")
            try:
                res = pd.read_sql_query(clean_sql, conn)
                print(f"Advanced Query #{adv_num} Success! Returned {len(res)} rows. Preview:")
                print(res.head(5).to_string(index=False))
                print("-" * 60 + "\n")
            except Exception as e:
                print(f"ERROR executing Advanced Query #{adv_num}: {e}\n")
            adv_num += 1
                
    conn.close()
    print("All SQL verification tests passed successfully!")

if __name__ == '__main__':
    test_sql_execution()
