import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import requests
import io

# Page config
st.set_page_config(page_title="🏡 Real Estate Price Prediction", layout="wide")

# Load data and model
@st.cache_data(show_spinner=False)
def load_data_model():
    # Load dataframe locally
    with open("datasets/page_1/df.pkl", "rb") as f:
        df_loaded = pickle.load(f)

    # Load model from URL
    url = "https://github.com/Yashrajgithub/Real-Estate-Application/raw/main/xgbmodel.pkl"
    response = requests.get(url)
    response.raise_for_status()  # Check that request succeeded

    model_bytes = io.BytesIO(response.content)
    model_loaded = pickle.load(model_bytes)

    return df_loaded, model_loaded
    
df, pipeline = load_data_model()

# --- CSS styling ---
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9f9f9;
    }
    h1 {
        color: #1f77b4;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0.2em;
    }
    h3 {
        color: #444444;
        margin-top: 1em;
    }
    .info-box {
        background-color: #ffffff;
        border-left: 5px solid #1f77b4;
        padding: 1em;
        margin-bottom: 1em;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #145a86;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("Real Estate Price Prediction 🏡")
st.markdown("<center><i style='color:red;'>Note: This price prediction tool is currently limited to properties in **Pune city** only.</i></center>", unsafe_allow_html=True)

# Main image
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.image("datasets/page_1/images.jpg")

# Sidebar info
with st.sidebar:
    st.header("📊 Model Details")
    st.markdown("""
    - **Accuracy:** 93.57% (R² Score)  
    - **MAE:** 0.17  
    - **Source:** [99acres.com](https://www.99acres.com)
    """)
    st.markdown("---")
    st.info("ℹ️ Navigate using the page menu if hidden.")

# Guidelines expander
with st.expander("📋 Guidelines"):
    st.markdown("""
    - Fill in **all property fields**.
    - Choose `"Not Known"` for unknown features.
    - Binary options like Pooja/Servant Room use `1` (Yes) or `0` (No).
    """)

# Input section
st.markdown("## 🏠 Enter Property Details")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location & Size")
    location = st.selectbox("Location", sorted(df['location'].unique()))
    built_up_area = st.number_input("Built-up Area (sq. ft)", min_value=200, step=50, value=1000)

    st.subheader("🏢 Property Details")
    bedrooms = float(st.selectbox("Bedrooms", sorted(df['bedrooms'].unique())))
    bathrooms = float(st.selectbox("Bathrooms", sorted(df['bathrooms'].unique())))
    balconies = float(st.selectbox("Balconies", sorted(df['balconies'].unique())))
    age_of_property = float(st.selectbox("Age of Property", sorted(df['age_of_property'].unique())))

with col2:
    st.subheader("🔧 Amenities & Features")
    storage_room = float(st.selectbox("Servant Room (0-No, 1-Yes)", [0.0, 1.0]))
    pooja_room = float(st.selectbox("Pooja Room (0-No, 1-Yes)", [0.0, 1.0]))
    furnishing_status = st.selectbox("Furnishing", ['Not Known'] + sorted(df['furnishing_status'].unique()))
    parking_space = st.selectbox("Parking Type", ['Not Known'] + sorted(df['parking_space'].unique()))
    flooring_type = st.selectbox("Flooring Type", ['Not Known'] + sorted(df['flooring_type'].unique()))
    luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique()))
    floor_category = st.selectbox("Floor Category", sorted(df['floor_category'].unique()))

# Initialize download_df in session_state
if "download_df" not in st.session_state:
    st.session_state.download_df = None

# Prediction and Reset buttons
col_pred, col_reset = st.columns([1, 1])

with col_pred:
    if st.button("Predict Price"):
        input_data = pd.DataFrame({
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'balconies': [balconies],
            'age_of_property': [age_of_property],
            'furnishing_status': [furnishing_status],
            'flooring_type': [flooring_type],
            'parking_space': [parking_space],
            'built_up_area': [built_up_area],
            'storage_room': [storage_room],
            'pooja_room': [pooja_room],
            'location': [location],
            'floor_category': [floor_category],
            'luxury_category': [luxury_category]
        })

        # Model prediction
        pred_log = pipeline.predict(input_data)[0]
        pred_price = np.exp(pred_log)  # inverse log transform

        # Format price nicely
        if pred_price < 1:
            price_str = f"₹ {round(pred_price * 100, 2)} Lakhs"
        else:
            price_str = f"₹ {round(pred_price, 2)} Crores"

        st.success(f"💰 **Estimated Price:** {price_str}")

        # Save for display & download
        result_df = input_data.copy()
        result_df.insert(0, "Predicted Price", price_str)

        st.dataframe(result_df)
        st.session_state.download_df = result_df

with col_reset:
    if st.button("↺ Reset Inputs"):
        st.session_state.download_df = None
        st.experimental_rerun()

# Download button outside columns
if st.session_state.download_df is not None:
    csv_data = st.session_state.download_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Prediction Result",
        data=csv_data,
        file_name="predicted_price.csv",
        mime='text/csv'
    )
