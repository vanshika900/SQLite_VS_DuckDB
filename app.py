import streamlit as st
import pandas as pd
import duckdb
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="SQLite vs DuckDB Benchmark", layout="wide")

st.title("SQLite vs. DuckDB Performance Lab")
st.markdown("""
This dashboard compares a **Row-Store (SQLite)** against a **Columnar-Store (DuckDB)** 
using the NYC Taxi Dataset (1M to 10M rows).
""")

st.sidebar.header("Dashboard Settings")
show_raw_data = st.sidebar.checkbox("Show Raw Results CSV")

@st.cache_data
def load_results():
    return pd.read_csv('benchmark_results.csv')

df = load_results()

if show_raw_data:
    st.subheader("Raw Benchmark Data")
    st.dataframe(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Latency Scalability")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='Scale', y='Time', hue='Database', marker='o', ax=ax)
    ax.set_ylabel("Seconds")
    st.pyplot(fig)

with col2:
    st.subheader("Peak Memory Usage (10M Rows)")
    fig, ax = plt.subplots()
    df_10m = df[df['Scale'] == 10000000]
    sns.barplot(data=df_10m, x='Query', y='Memory_MB', hue='Database', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()
st.header("Live 'Explain Plan' Explorer")
st.info("Select a query to see how the database optimizers handle it differently.")

query_choice = st.selectbox("Choose a Query Type", [
    "SELECT AVG(fare_amount) FROM {table}",
    "SELECT COUNT(*) FROM {table} WHERE passenger_count > 2",
    "SELECT VendorID, SUM(total_amount) FROM {table} GROUP BY VendorID"
])

if st.button("Run Explain Plans"):
    table = "taxi_1000000" 

    dd_conn = duckdb.connect('test2_database.db')
    dd_plan = dd_conn.execute(f"EXPLAIN {query_choice.format(table=table)}").fetchall()
    dd_conn.close()
    
    sq_conn = sqlite3.connect('test_database.db')
    # We fetch all rows because SQLite breaks the plan into multiple steps
    sq_raw_plan = sq_conn.execute(f"EXPLAIN QUERY PLAN {query_choice.format(table=table)}").fetchall()
    sq_conn.close()
    
    # We combine the 'detail' column (index 3) from every row into one string
    sq_plan_text = ""
    for row in sq_raw_plan:
        sq_plan_text += f"-> {row[3]}\n" 

    c1, c2 = st.columns(2)
    with c1:
        st.write("**DuckDB Optimizer Path (Columnar):**")
        st.code(dd_plan[0][1]) # DuckDB returns a pre-formatted string here
    with c2:
        st.write("**SQLite Optimizer Path (Row-based):**")
        if sq_plan_text:
            st.code(sq_plan_text)
        else:
            st.code("No plan found. Ensure table exists.")