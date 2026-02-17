import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# Custom CSS for modern Tiles (Cards)
st.markdown("""
    <style>
    .feedback-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #333;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .rating-good { border-left-color: #2ecc71; }
    .rating-meh { border-left-color: #f1c40f; }
    .rating-bad { border-left-color: #e74c3c; }
    .feedback-text { font-style: italic; color: #444; margin-top: 10px; }
    .suggestion-text { font-weight: bold; color: #222; }
    .label { font-size: 0.8rem; color: #888; text-transform: uppercase; margin-bottom: 5px; }
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

    filtered_df = df[df['Newsletter'] == selected_issue]

    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    total_fb = len(filtered_df)
    good_count = len(filtered_df[filtered_df['Rating'] == "Good"])
    comment_count = filtered_df['Comments'].dropna().count() + filtered_df['Suggestions'].dropna().count()
    
    col1.metric("Total Feedbacks", total_fb)
    col2.metric("Positive Ratings", f"{good_count} (Good)")
    col3.metric("Written Comments", int(comment_count))

    st.write("") 

    # --- TILES SECTION ---
    st.subheader(f"What
