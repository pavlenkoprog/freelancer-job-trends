# notebooks/preprocessing.ipynb или отдельный .py файл
import pandas as pd
import sqlite3

# Загрузка parquet
df = pd.read_parquet("../data/freelancer_earnings.parquet")

# Сохранение в SQLite
conn = sqlite3.connect("../data/freelancer_earnings.db")
df.to_sql("freelancer_earnings", conn, if_exists="replace", index=False)
conn.close()
