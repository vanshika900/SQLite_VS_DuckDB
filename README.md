**SQLite vs. DuckDB: Analytical Performance Benchmark**
This project provides a comprehensive performance comparison between SQLite (a row-based RDBMS) and DuckDB (a columnar OLAP database). It evaluates how each engine handles analytical workloads, specifically focusing on query latency and memory consumption when processing large-scale datasets.

**📊 Overview**
The benchmark utilizes the NYC Taxi Dataset to simulate real-world data science tasks. By comparing a traditional transactional engine against a modern analytical one, this project demonstrates why columnar storage is often superior for heavy aggregations and data analysis.

**📁 Project Structure**
As seen in the workspace:

app.py: The main execution script for the benchmark suite.

benchmark.py: Core logic for timing queries and measuring engine performance.

loader.py: Handles data ingestion and database initialization.

visualize.py: Generates charts and plots from the benchmark results.

explain_plans.py: Provides insights into the query execution plans for both databases.

requirements.txt: Lists all necessary Python dependencies.

README.md: Project documentation.

**🚀 Getting Started**
1. Installation
Clone the repository and install the required packages:

Bash
pip install -r requirements.txt
2. Prepare Data
Run the loader to process the Parquet files and set up your local databases:

Bash
python loader.py
3. Run Benchmark
Execute the performance tests to generate timing data:

Bash
python benchmark.py
4. Generate Visuals
Create the comparison plots to see the results:

Bash
python visualize.py

**📈 Results & Visuals**
The suite generates several outputs for analysis:

latency_plot.png: A visual comparison of query execution times.

memory_bar_chart.png: A comparison of memory footprint during processing.

benchmark_results.csv: Raw performance metrics exported for further study.

**🛠 Tech Stack**
Database Engines: SQLite, DuckDB

Data Format: Apache Parquet

Language: Python 3.13

Libraries: Pandas, Matplotlib

To fix the display:
Delete everything currently in your README.md file in VS Code.

Paste the text above.

Save the file.

In Git Bash, run:

Bash
git add README.md
git commit -m "Fixing README formatting"
git push origin main
