import pandas as pd
import sqlite3
import duckdb

# 1. Load the big CSV once
print("Reading taxi_data.csv...")
df = pd.read_csv('taxi_data.csv')

scales = [1000000, 5000000, 10000000]

for limit in scales:
    print(f"Processing scale: {limit} rows...")
    subset = df.head(limit)
    table_name = f"taxi_{limit}"
    
    conn_sq = sqlite3.connect('test_database.db')
    subset.to_sql(table_name, conn_sq, if_exists='replace', index=False)
    conn_sq.close()
    
    conn_dd = duckdb.connect('test2_database.db')
    # DuckDB can "see" the 'subset' variable in your memory
    conn_dd.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM subset")
    conn_dd.close()

print("Phase 1 Complete: All tables created in both databases.")