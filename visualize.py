import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the results from your benchmark
df = pd.read_csv('benchmark_results.csv')

# --- Chart 1: Latency (Line Plot) ---
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Scale', y='Time', hue='Database', marker='o')
plt.title('Execution Latency vs Dataset Scale')
plt.ylabel('Time (Seconds)')
plt.xlabel('Number of Rows')
plt.grid(True)
plt.savefig('latency_plot.png')
print("Saved latency_plot.png")
# plt.show() # Commented out so it doesn't freeze your terminal

# --- Chart 2: Memory (Bar Chart for 10M rows) ---
plt.figure(figsize=(12, 6))
df_10m = df[df['Scale'] == 10000000]
sns.barplot(data=df_10m, x='Query', y='Memory_MB', hue='Database')
plt.xticks(rotation=45)
plt.title('Peak Memory Usage at 10M Rows')
plt.tight_layout()
plt.savefig('memory_bar_chart.png')
print("Saved memory_bar_chart.png")
# plt.show()