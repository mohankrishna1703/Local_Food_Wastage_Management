# scripts/run_queries.py
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parents[1] / "local_food.db"

def run_and_print(sql):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        print("SQL:\n", sql)
        print(df.head(10).to_string(index=False))
        print("\n" + "-"*60 + "\n")
    finally:
        conn.close()

if __name__ == "__main__":
    sql_file = Path(__file__).parents[1] / "queries.sql"
    with open(sql_file) as f:
        queries = [q.strip() for q in f.read().split(";") if q.strip()]
    for q in queries:
        run_and_print(q + ";")