# scripts/create_db.py
import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parents[1]
DATA_DIR = BASE / "data"
DB_PATH = BASE / "local_food.db"

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
    DROP TABLE IF EXISTS providers;
    DROP TABLE IF EXISTS receivers;
    DROP TABLE IF EXISTS food_listings;
    DROP TABLE IF EXISTS claims;

    CREATE TABLE providers(
        Provider_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    );

    CREATE TABLE receivers(
        Receiver_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    );

    CREATE TABLE food_listings(
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date TEXT,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT,
        FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
    );

    CREATE TABLE claims(
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp TEXT,
        FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
        FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
    );
    """)

    # Load CSVs with pandas and insert
    pd.read_csv(DATA_DIR / "providers_data.csv").to_sql("providers", conn, if_exists="append", index=False)
    pd.read_csv(DATA_DIR / "receivers_data.csv").to_sql("receivers", conn, if_exists="append", index=False)
    pd.read_csv(DATA_DIR / "food_listings_data.csv").to_sql("food_listings", conn, if_exists="append", index=False)
    pd.read_csv(DATA_DIR / "claims_data.csv").to_sql("claims", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")

if __name__ == "__main__":
    create_db()