import pyarrow.parquet as pq
import pandas as pd

df1 = pd.read_parquet('yellow_tripdata_2026.parquet')
df3 = pd.read_parquet('yellow_tripdata_202601.parquet')
df2 = pd.read_parquet('yellow_tripdata_202602.parquet')

combined_df = pd.concat([df1, df2, df3], ignore_index=True)
combined_df.to_csv('taxi_data.csv', index=False)