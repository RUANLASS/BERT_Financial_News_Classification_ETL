# data_load.py
import prefect
from prefect import task
import pandas as pd
import sqlite3

@task
def load_to_csv(df: pd.DataFrame, filepath: str = "cleaned_news.csv") -> None:
    """Save dataframe to CSV."""
    df.to_csv(filepath, index=False)
    print(f"✅ Data saved to {filepath}")

@task
def load_to_sqlite(df: pd.DataFrame, db_path: str = "news.db", table_name: str = "news") -> None:
    """Save dataframe to a SQLite database."""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Data saved to {db_path} in table '{table_name}'")
