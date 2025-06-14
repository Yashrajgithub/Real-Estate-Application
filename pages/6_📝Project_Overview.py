import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

DB_FILE = Path("datasets/page_5/feedback.db").resolve()

# --- Database Functions ---
def create_connection():
    return sqlite3.connect(DB_FILE)

def create_feedback_table():
    conn = create_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS feedback 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     feedback TEXT, 
                     rating REAL)''')
    conn.commit()
    conn.close()

def load_feedback():
    create_feedback_table()
    conn = create_connection()
    df = pd.read_sql("SELECT name, feedback, rating FROM feedback", conn)
    conn.close()
    return df

def save_feedback(name, feedback, rating):
    create_feedback_table()
    conn = create_connection()
    conn.execute("INSERT INTO feedback (name, feedback, rating) VALUES (?, ?, ?)", (name, feedback, rating))
    conn.commit()
    conn.close()

def check_feedback_submitted():
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

# --- Main Page ---
def main():
    check_feedback_submitted()

    # --- Custom Styling ---
    st.markdown("""
        <style>
            .main-title {
                font-size: 40px;
                text-align: center;
                color: #4B8BBE;
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 26px;
                color: #FF7F50;
                margin-top: 30px;
                margin-bottom: 10px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
            .rating-info {
                color: #888;
                font-size: 14px;
                margin-top: -10px;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>📊 Project Overview & Feedback</div>", unsafe_allow_html=True)

    # --- GitHub Link Only ---
    st.markdown("<div class='section-title'>💻 Project Repository</div>", unsafe_allow_html=True)
    st.markdown("[🔗 GitHub Repository](https://github.com/Yashrajgithub/Real-Estate-Application.git)", unsafe_allow_html=True)
    st.info("⭐ If you like the work, please star the GitHub repo.")


    # --- Feedback Form ---
    st.markdown("<div class='section-title'>📝 Share Your Feedback</div>", unsafe_allow_html=True)

    if not st.session_state.feedback_submitted:
        with st.form("feedback_form"):
            name = st.text_input("Your Name", placeholder="e.g. John Doe")
            feedback = st.text_area("Your Feedback", placeholder="Write something insightful...")
            rating = st.slider("Rating (1 = Worst, 5 = Best)", 1.0, 5.0, 4.5, step=0.1)
            st.markdown("<div class='rating-info'>Rate your experience with the project.</div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Submit Feedback", type="primary")

            if submit:
                if name.strip() and feedback.strip():
                    save_feedback(name.strip(), feedback.strip(), rating)
                    st.success("✅ Thank you for your feedback!")
                    st.session_state.feedback_submitted = True
                else:
                    st.warning("⚠️ Please provide both name and feedback.")

    else:
        st.success("✅ Feedback already submitted. Thanks!")

    # --- View All Feedback (optional) ---
    with st.expander("📬 View All Feedback"):
        df = load_feedback()
        st.dataframe(df)

if __name__ == "__main__":
    main()
