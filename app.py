import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# Custom CSS for Pinterest-style layout
st.markdown("""
    <style>
    .feedback-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        border-top: 6px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        min-height: 100px;
    }
    .rating-good { border-top-color: #2ecc71; }
    .rating-meh { border-top-color: #f1c40f; }
    .rating-bad { border-top-color: #e74c3c; }
    .feedback-text { font-style: italic; color: #444; margin-top: 12px; font-size: 0.95rem; line-height: 1.4; }
    .suggestion-text { font-weight: bold; color: #222; margin-top: 5px; }
    .label { font-size: 0.7rem; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; }
    .card-date { color: #bbb; font-size: 0.75rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Gents Cafe Reader Feedback")

@st.cache_data
def load_data():
    file_name = "feedback.csv" 
    df = pd.read_csv(file_name)
    df.columns = [
        'Newsletter', 'Archive', 'Created_time', 'Email_Metadata', 'Email', 
        'Rating', 'Suggestions', 'Comments'
    ]
    df['Created_time'] = pd.to_datetime(df['Created_time'])
    return df

try:
    df = load_data()

    # --- TOP SELECTION MENU ---
    st.markdown("---")
    newsletter_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()
    
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        selected_issue = st.selectbox("Select a Newsletter Issue:", newsletter_list)
    st.markdown("---")

    # Data for the metrics (all feedbacks)
    issue_df = df[df['Newsletter'] == selected_issue]
    
    # Data for the Tiles (only with text)
    text_df = issue_df[issue_df['Comments'].notnull() | issue_df['Suggestions'].notnull()].copy()

    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    total_fb = len(issue_df)
    good_count = len(issue_df[issue_df['Rating'] == "Good"])
    written_count = len(text_df)
    
    col1.metric("Total Feedbacks", total_fb)
    col2.metric("Positive Ratings", f"{good_count} (Good)")
    col3.metric("Feedback with Comments", written_count)

    st.write("") 

    # ---
