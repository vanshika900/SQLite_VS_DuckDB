import sqlite3
import duckdb

# SQLite Explain
print("--- SQLite Explain Plan ---")
conn_sq = sqlite3.connect('test_database.db')
plan_sq = conn_sq.execute("EXPLAIN QUERY PLAN SELECT AVG(fare_amount) FROM taxi_10000000").fetchall()
for row in plan_sq: print(row)
conn_sq.close()

# DuckDB Explain
print("\n--- DuckDB Explain Plan ---")
conn_dd = duckdb.connect('test2_database.db')
# DuckDB gives a beautiful detailed breakdown
plan_dd = conn_dd.execute("EXPLAIN ANALYZE SELECT AVG(fare_amount) FROM taxi_10000000").fetchall()
print(plan_dd[0][1]) 
conn_dd.close()