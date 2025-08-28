import streamlit as st
import requests
import pandas as pd

# ---------------------------
# Config
# ---------------------------
API_URL = "http://127.0.0.1:8000/predict"  # FastAPI backend ka endpoint

# Dropdown values (static from training data)
AREA_TYPES = [
    "Super built-up  Area",
    "Plot  Area",
    "Built-up  Area",
    "Carpet  Area"
]

# Location list (you can load dynamically from CSV or hardcode for now)
LOCATIONS = [
    "Electronic City Phase II", "Chikka Tirupathi", "Uttarahalli", 
    "Lingadheeranahalli", "Kothanur", "Whitefield", "Old Airport Road",
    "Rajaji Nagar", "Marathahalli", "other", "7th Phase JP Nagar",
    "Gottigere", "Sarjapur", "Mysore Road", "Bisuvanahalli",
    # 🔽 You can load complete list from file if too big
]

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🏠 House Price Prediction", layout="centered")
st.title("🏠 Bangalore House Price Prediction")
st.markdown("Enter the house details to predict its price")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        area_type = st.selectbox("Area Type", AREA_TYPES)
        location = st.selectbox("Location", LOCATIONS, index=0)
        total_sqft = st.number_input("Total Sqft", min_value=200.0, max_value=10000.0, step=10.0)

    with col2:
        bath = st.number_input("Bathrooms", min_value=1, max_value=10, step=1)
        bhk = st.number_input("BHK", min_value=1, max_value=10, step=1)

    submitted = st.form_submit_button("🔍 Predict Price")

# ---------------------------
# Call FastAPI Backend
# ---------------------------
if submitted:
    input_data = {
        "area_type": area_type,
        "location": location,
        "total_sqft": total_sqft,
        "bath": bath,
        "bhk": bhk
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            predicted_price = result.get("predicted_price")

            st.success(f"💰 Predicted Price: **{predicted_price:.2f} Lakhs**")
        else:
            st.error(f"API Error: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
