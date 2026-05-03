import sqlite3
import duckdb
import time
import tracemalloc
import pandas as pd

queries = {
    "1_Avg_Fare": "SELECT AVG(fare_amount) FROM {table}",
    "2_Trips_Per_Vendor": "SELECT VendorID, COUNT(*) FROM {table} GROUP BY VendorID",
    "3_Complex_Filter": "SELECT COUNT(*) FROM {table} WHERE passenger_count > 2 AND trip_distance > 10",
    "4_High_Value_Sort": "SELECT * FROM {table} ORDER BY total_amount DESC LIMIT 500",
    "5_Window_Rank": "SELECT AVG(fare_amount) OVER(PARTITION BY VendorID) FROM {table} LIMIT 500",
    "6_Self_Join": "SELECT a.VendorID, b.total_amount FROM {table} a JOIN {table} b ON a.tpep_pickup_datetime = b.tpep_pickup_datetime LIMIT 500",
    "7_Distinct_Locations": "SELECT COUNT(DISTINCT PULocationID) FROM {table}",
    "8_Tip_Sum": "SELECT SUM(tip_amount) FROM {table} WHERE payment_type = 1"
}

scales = [1000000, 5000000, 10000000]
results = []

def measure(db_type, conn, q_name, sql):
    tracemalloc.start()
    start = time.perf_counter()
    
    conn.execute(sql).fetchall()
    
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end - start, peak / (1024 * 1024)

for scale in scales:
    print(f"Benchmarking {scale} rows...")
    sq_conn = sqlite3.connect('test_database.db')
    dd_conn = duckdb.connect('test2_database.db')
    
    for q_name, template in queries.items():
        sql = template.format(table=f"taxi_{scale}")
        
        # Test SQLite
        t, m = measure("SQLite", sq_conn, q_name, sql)
        results.append({"Database": "SQLite", "Scale": scale, "Query": q_name, "Time": t, "Memory_MB": m})
        
        # Test DuckDB
        t, m = measure("DuckDB", dd_conn, q_name, sql)
        results.append({"Database": "DuckDB", "Scale": scale, "Query": q_name, "Time": t, "Memory_MB": m})

    sq_conn.close()
    dd_conn.close()

pd.DataFrame(results).to_csv('benchmark_results.csv', index=False)
print("Phase 2 Complete: Results saved to benchmark_results.csv")