# streamlit_app.py
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("local_food.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

@st.cache_data
def load_tables():
    conn = get_conn()
    providers = pd.read_sql("SELECT * FROM providers", conn)
    receivers = pd.read_sql("SELECT * FROM receivers", conn)
    food = pd.read_sql("SELECT * FROM food_listings", conn, parse_dates=["Expiry_Date"])
    claims = pd.read_sql("SELECT * FROM claims", conn, parse_dates=["Timestamp"])
    conn.close()
    return providers, receivers, food, claims

st.set_page_config(page_title="Local Food Wastage Management", layout="wide")
st.title("Local Food Wastage Management System (Beginner Level)")

providers, receivers, food, claims = load_tables()

st.sidebar.header("Filters")
city = st.sidebar.selectbox("City", options=["All"] + sorted(food['Location'].dropna().unique().tolist()))
food_type = st.sidebar.selectbox("Food Type", options=["All"] + sorted(food['Food_Type'].dropna().unique().tolist()))
meal_type = st.sidebar.selectbox("Meal Type", options=["All"] + sorted(food['Meal_Type'].dropna().unique().tolist()))

filtered = food.copy()
if city != "All":
    filtered = filtered[filtered['Location'] == city]
if food_type != "All":
    filtered = filtered[filtered['Food_Type'] == food_type]
if meal_type != "All":
    filtered = filtered[filtered['Meal_Type'] == meal_type]

st.subheader("Available Food Listings")
st.dataframe(filtered)

st.subheader("Provider Contact Details")
provider_id = st.number_input("Enter Provider ID to view contact", min_value=1, step=1)
if st.button("Show Contact"):
    p = providers[providers['Provider_ID'] == provider_id]
    if not p.empty:
        st.write(p[['Name', 'Contact', 'Address', 'City']].iloc[0].to_dict())
    else:
        st.warning("Provider not found")

st.sidebar.subheader("Add New Food Listing (simple)")
with st.sidebar.form("add_food"):
    fid = st.number_input("Food ID", min_value=1, step=1)
    name = st.text_input("Food Name")
    qty = st.number_input("Quantity", min_value=1, step=1)
    expiry = st.date_input("Expiry Date", value=datetime.today())
    provider_id_input = st.number_input("Provider ID", min_value=1, step=1)
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location")
    food_type_input = st.text_input("Food Type")
    meal_type_input = st.text_input("Meal Type")
    submitted = st.form_submit_button("Add listing")
    if submitted:
        conn = get_conn()
        try:
            conn.execute("""
                INSERT INTO food_listings(Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(fid), name, int(qty), expiry.isoformat(), int(provider_id_input), provider_type, location, food_type_input, meal_type_input))
            conn.commit()
            st.success("Listing added. Refresh app to see changes.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()

st.markdown("---")
st.subheader("Claims (recent)")
st.dataframe(claims.sort_values(by="Timestamp", ascending=False).head(20))