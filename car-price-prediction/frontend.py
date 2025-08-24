# streamlit_app.py
import streamlit as st
import requests

# --------------------------
# Config
# --------------------------
API_URL = "http://127.0.0.1:8000/predict"  # FastAPI local URL

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="centered")

st.title("🚗 Car Price Prediction")
st.markdown("Enter car details to predict the price using the trained ML model.")

# --------------------------
# Sidebar Input
# --------------------------
st.sidebar.header("Car Features")

make = st.sidebar.selectbox("Make", ["Honda", "Ford", "BMW", "Toyota", "Other"])
model = st.sidebar.text_input("Model", value="Model B")
fuel_type = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric", "Hybrid"])
transmission = st.sidebar.selectbox("Transmission", ["Manual", "Automatic"])
year = st.sidebar.number_input("Year", min_value=1990, max_value=2025, value=2015)
engine_size = st.sidebar.number_input("Engine Size (L)", min_value=0.5, max_value=8.0, step=0.1, value=3.9)
dist_driven = st.sidebar.number_input("Distance Driven (km)", min_value=0, max_value=300000, value=74176)

# --------------------------
# Predict Button
# --------------------------
if st.sidebar.button("🔍 Predict Price"):
    input_data = {
        "Make": make,
        "Model": model,
        "Fuel_Type": fuel_type,
        "Transmission": transmission,
        "Year": year,
        "Engine_Size": engine_size,
        "Dist_Driven": dist_driven
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            if "predicted_price" in result:
                st.success(f"💰 Estimated Price: **${result['predicted_price']:.2f}**")
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# --------------------------
# Footer
# --------------------------
st.markdown("---")
st.caption("Powered by FastAPI + Streamlit 🚀")
