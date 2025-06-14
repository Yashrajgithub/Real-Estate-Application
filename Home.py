import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st
from PIL import Image
from pathlib import Path
import sqlite3
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Homematch AI",
    page_icon="🏠",
    layout="wide",
)

DB_FILE = Path("datasets/page_5/feedback.db").resolve()

# --- Database Functions ---
def create_connection():
    return sqlite3.connect(DB_FILE)

def create_feedback_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            feedback TEXT,
            rating INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def load_feedback():
    create_feedback_table()
    conn = create_connection()
    df = pd.read_sql_query("SELECT name, feedback, rating FROM feedback", conn)
    conn.close()
    return df

def calculate_feedback_stats(df):
    avg_rating = df['rating'].mean() if not df.empty else 0
    review_count = df.shape[0]
    return avg_rating, review_count

# --- Load Feedback and Sidebar Display ---
feedback_df = load_feedback()
avg_rating, review_count = calculate_feedback_stats(feedback_df)

st.sidebar.markdown("""
    <style>
        .sidebar-content {
            background-color: #fdf6e3;
            padding: 20px;
            border-radius: 10px;
            color: #333;
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
    <div class="sidebar-content">
        <h3 style="text-align: center;">📊 Feedback Summary</h3>
        <p style="font-size: 18px;"><strong>⭐ Average Rating:</strong> {avg_rating:.2f}</p>
        <p style="font-size: 18px;"><strong>📝 Total Reviews:</strong> {review_count}</p>
        <hr>
        <span style='color: #b58900;'>⬇️ Use the menu above to navigate</span>
    </div>
""", unsafe_allow_html=True)

# --- Header Section with Gradient Title ---
st.markdown("""
    <style>
        .gradient-text {
            font-weight: bold;
            font-size: 42px;
            background: linear-gradient(270deg, #4FC3F7, #00BCD4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: transparent;
            display: inline;
        }
    </style>

    <h1 style='text-align: center;'>
        🏠 <span class="gradient-text">Homematch AI Application</span>
    </h1>
""", unsafe_allow_html=True)

# --- Main Content ---
def main():
    image_path = Path("datasets/home_page/homepage_img.jpeg")  # Define before checking
    if image_path.exists():
        image = Image.open(image_path)
        resized_image = image.resize((900, 450))
        st.image(resized_image)
    else:
        st.warning(f"Image not found at path: {image_path}")

    # Welcome Section with Gradient Text
    st.markdown("""
        <style>
            .gradient-h2 {
                font-size: inherit;
                font-weight: bold;
                background: linear-gradient(270deg, #4FC3F7, #00BCD4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                color: transparent;
            }

            .gradient-p {
                font-size: inherit;
                background: linear-gradient(270deg, #4FC3F7, #00BCD4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                color: transparent;
            }
        </style>

        <div style='text-align: center; margin-top: 30px;'>
            <h2><span class='gradient-h2'>Welcome to Homematch AI!</span></h2>
            <p style='font-size: 18px;'>
                <span class='gradient-p'>
                    Explore property insights, predictions, and recommendations tailored to Pune’s real estate market.
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Overview
    st.markdown("---")
    st.subheader("🚀 Features Overview")
    st.markdown("""
        - 🏷️ **Price Prediction** – Predict future property prices using ML models.
        - 🏘️ **Property Recommendation** – Get recommendations based on location, features, and user preferences.
        - 📈 **Analytics Dashboard** – Interactive graphs, charts, and maps.
        - 📊 **Market Insights** – Stay updated with Pune's real estate trends.
        - 🧾 **Final Report** – Summarized reports with conclusions.
    """)

    # Guidelines
    st.markdown("---")
    st.subheader("📜 Guidelines for Best Use")
    st.markdown("""
        - Navigate using the left panel.
        - Enter correct data for accurate results.
        - Use filters to refine property searches.
        - In recommendations, explore various strategies (location-based, facilities-based, etc.).
        - Visualize insights through the analytics tab.
        - Don't forget to leave feedback on the final page!
    """)

# --- App Entry Point ---
if __name__ == "__main__":
    main()
