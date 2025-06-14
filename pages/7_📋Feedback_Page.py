import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import yaml

# Load configuration
path_ = Path("datasets/page_3/config.yaml")
with open(path_, "r") as f:
    config = yaml.safe_load(f)
HOST_PASSWORD = config.get("HOST_PASSWORD")

DB_FILE = Path("datasets/page_5/feedback.db").resolve()

def create_connection():
    return sqlite3.connect(DB_FILE)

def create_feedback_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, feedback TEXT, rating INTEGER)''')
    conn.commit()
    conn.close()

def load_feedback():
    create_feedback_table()
    conn = create_connection()
    df = pd.read_sql_query("SELECT id, name, feedback, rating FROM feedback", conn)
    conn.close()
    return df

def delete_feedback(feedback_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    conn.commit()
    conn.close()

def main():
    # Dark theme compatible styles
    st.markdown("""
        <style>
            .section-title {
                font-size: 30px;
                font-weight: 700;
                border-bottom: 3px solid #00b894;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            .feedback-box {
                border: 1px solid #444;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                background-color: #1e1e1e;
                box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            }
            .feedback-box .name {
                color: #74b9ff;
                font-size: 18px;
                font-weight: bold;
            }
            .feedback-box .rating {
                color: #fdcb6e;
                font-size: 16px;
            }
            .feedback-box .comment {
                color: #dfe6e9;
                font-size: 16px;
                margin-top: 5px;
            }
            .thank-you {
                background-color: #2d3436;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
                text-align: center;
                font-size: 18px;
                color: #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📋 Feedback Wall</div>", unsafe_allow_html=True)
    
    feedback_df = load_feedback()
    if feedback_df.empty:
        st.warning("No feedback available yet. Be the first to give your thoughts! 😊")
    else:
        st.info(f"Showing {len(feedback_df)} feedback entries")

        st.sidebar.header("🔐 Admin Login")
        password = st.sidebar.text_input("Enter password", type="password")
        is_host = password == HOST_PASSWORD

        if password and not is_host:
            st.sidebar.error("Access Denied")

        for _, row in feedback_df.iterrows():
            st.markdown(f"""
                <div class='feedback-box'>
                    <div class='name'>👤 {row['name']}</div>
                    <div class='rating'>⭐ Rating: {row['rating']}</div>
                    <div class='comment'>💬 {row['feedback']}</div>
                </div>
            """, unsafe_allow_html=True)

            if is_host:
                if st.button("🗑️ Delete", key=f"delete_{row['id']}"):
                    delete_feedback(row['id'])
                    st.experimental_rerun()

    st.markdown("""
        <div class='thank-you'>
            🙏 Thank you for your feedback! Your insights help us grow and improve 💡
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
