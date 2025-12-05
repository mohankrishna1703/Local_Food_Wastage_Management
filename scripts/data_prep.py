# scripts/data_prep.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parents[1] / "data"

def load_and_clean():
    # Load CSVs
    providers = pd.read_csv(DATA_DIR / "providers_data.csv")
    receivers = pd.read_csv(DATA_DIR / "receivers_data.csv")
    food = pd.read_csv(DATA_DIR / "food_listings_data.csv")
    claims = pd.read_csv(DATA_DIR / "claims_data.csv", parse_dates=["Timestamp"])

    # Basic cleaning examples:
    providers['City'] = providers['City'].str.strip().str.title()
    receivers['City'] = receivers['City'].str.strip().str.title()
    food['Location'] = food['Location'].str.strip().str.title()
    food['Expiry_Date'] = pd.to_datetime(food['Expiry_Date'], errors='coerce')

    # Ensure IDs are integers
    providers['Provider_ID'] = providers['Provider_ID'].astype(int)
    receivers['Receiver_ID'] = receivers['Receiver_ID'].astype(int)
    food['Food_ID'] = food['Food_ID'].astype(int)
    claims['Claim_ID'] = claims['Claim_ID'].astype(int)

    return providers, receivers, food, claims

if __name__ == "__main__":
    p, r, f, c = load_and_clean()
    print("Providers:", len(p))
    print("Receivers:", len(r))
    print("Food listings:", len(f))
    print("Claims:", len(c))