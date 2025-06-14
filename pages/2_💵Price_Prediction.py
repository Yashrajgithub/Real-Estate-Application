import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Set page configuration
st.set_page_config(page_title="🏡 Real Estate Price Prediction", layout="wide")

# Cache loading of model and dataframe to avoid repeated reloads
@st.cache_data
def load_model_and_data():
    with open(Path("datasets/page_1/df.pkl"), "rb") as f:
        df_loaded = pickle.load(f)
    with open(Path("datasets/page_1/xgbmodel.pkl"), "rb") as f:
        pipeline_loaded = pickle.load(f)
    return df_loaded, pipeline_loaded

df, pipeline = load_model_and_data()

# Initialize session state for download dataframe
if 'download_df' not in st.session_state:
    st.session_state['download_df'] = None

# ---------- Custom CSS ----------
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
    .main-image {
        border-radius: 12px;
        margin-bottom: 30px;
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

# ---------- Header ----------
st.title("Real Estate Price Prediction 🏡")
st.markdown("<center><i style='color:red;'>Note: This price prediction tool is currently limited to properties in **Pune city** only.</i></center>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.image("datasets/page_1/images.jpg", use_container_width=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("📊 Model Details")
    st.markdown("""
    - **Accuracy:** 93.57% (R² Score)  
    - **MAE:** 0.17  
    - **Source:** [99acres.com](https://www.99acres.com)
    """)
    st.markdown("---")
    st.info("ℹ️ Navigate using the page menu if hidden.")

# ---------- Guidelines ----------
with st.expander("📋 Guidelines"):
    st.markdown("""
    - Fill in **all property fields**.
    - Choose `"Not Known"` for unknown features.
    - Binary options like Pooja/Servant Room use `1` (Yes) or `0` (No).
    """)

# ---------- Input Section ----------
st.markdown("## 🏠 Enter Property Details")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location & Size")
    location = st.selectbox("Location", sorted(df['location'].unique()))
    built_up_area = st.number_input("Built-up Area (sq. ft)", min_value=200, step=50, value=1000)

    st.subheader("🏢 Property Details")
    bedrooms = int(st.selectbox("Bedrooms", sorted(df['bedrooms'].unique())))
    bathrooms = int(st.selectbox("Bathrooms", sorted(df['bathrooms'].unique())))
    balconies = int(st.selectbox("Balconies", sorted(df['balconies'].unique())))
    age_of_property = st.selectbox("Age of Property", sorted(df['age_of_property'].unique()))

with col2:
    st.subheader("🔧 Amenities & Features")
    storage_room = int(st.selectbox("Servant Room (0-No, 1-Yes)", [0, 1]))
    pooja_room = int(st.selectbox("Pooja Room (0-No, 1-Yes)", [0, 1]))
    furnishing_status = st.selectbox("Furnishing", ['Not Known'] + sorted(df['furnishing_status'].unique()))
    parking_space = st.selectbox("Parking Type", ['Not Known'] + sorted(df['parking_space'].unique()))
    flooring_type = st.selectbox("Flooring Type", ['Not Known'] + sorted(df['flooring_type'].unique()))
    luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique()))
    floor_category = st.selectbox("Floor Category", sorted(df['floor_category'].unique()))

# ---------- Prediction Section ----------
st.markdown("### Prediction")

col_pred, col_reset = st.columns([1, 1])

with col_pred:
    if st.button("Predict Price"):
        data = [[
            bedrooms, bathrooms, balconies, age_of_property, furnishing_status,
            flooring_type, parking_space, built_up_area, storage_room, pooja_room,
            location, floor_category, luxury_category
        ]]
        cols = [
            'bedrooms', 'bathrooms', 'balconies', 'age_of_property', 'furnishing_status',
            'flooring_type', 'parking_space', 'built_up_area', 'storage_room',
            'pooja_room', 'location', 'floor_category', 'luxury_category'
        ]

        df_input = pd.DataFrame(data, columns=cols)

        # Predict using the loaded pipeline
        price = np.exp(pipeline.predict(df_input))[0]

        # Price formatting
        if price < 1:
            price_text = f"₹ {round(price * 100, 2)} Lakhs"
        else:
            price_text = f"₹ {round(price, 2)} Crores"

        st.success(f"💰 **Estimated Price:** {price_text}")

        # Add predicted price to dataframe for display and download
        df_input.insert(0, "Predicted Price", price_text)
        st.dataframe(df_input)

        # Save prediction result for download
        st.session_state['download_df'] = df_input.copy()

with col_reset:
    if st.button("↺ Reset Inputs"):
        st.session_state['download_df'] = None
        st.experimental_rerun()

# ---------- Download Button ----------
if st.session_state['download_df'] is not None:
    csv = st.session_state['download_df'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Prediction Result",
        data=csv,
        file_name="predicted_price.csv",
        mime='text/csv'
    )
