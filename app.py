import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# Custom CSS for Pinterest-style layout (Focus on Comments)
st.markdown("""
    <style>
    .feedback-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        border-top: 6px solid #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .rating-good { border-top-color: #2ecc71; }
    .rating-meh { border-top-color: #f1c40f; }
    .rating-bad { border-top-color: #e74c3c; }
    .feedback-text { 
        font-family: 'Georgia', serif;
        font-style: italic; 
        color: #333; 
        margin-top: 15px; 
        font-size: 1.1rem; 
        line-height: 1.6; 
    }
    .label { 
        font-size: 0.7rem; 
        color: #aaa; 
        text-transform: uppercase; 
        letter-spacing: 1.2px; 
        margin-bottom: 8px; 
    }
    .card-date { color: #ccc; font-size: 0.75rem; }
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

    # Full data for metrics
    issue_df = df[df['Newsletter'] == selected_issue]
    
    # FILTER: Only feedbacks that have a COMMENT
    text_df = issue_df[issue_df['Comments'].notnull()].copy()

    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    total_fb = len(issue_df)
    good_count = len(issue_df[issue_df['Rating'] == "Good"])
    comments_shown = len(text_df)
    
    col1.metric("Total Feedbacks", total_fb)
    col2.metric("Positive Ratings", f"{good_count} (Good)")
    col3.metric("Comments to Read", comments_shown)

    st.write("") 

    # --- PINTEREST TILES SECTION ---
    st.subheader(f"Direct Reader Comments: {selected_issue}")

    if comments_shown == 0:
        st.info("No written comments found for this issue (only ratings).")
    else:
        # 3-column layout
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(text_df.iterrows()):
            col_index = i % 3
            
            r = str(row['Rating']).strip()
            rating_class = "rating-good" if r == "Good" else ("rating-meh" if r == "Meh" else "rating-bad")
            
            comment = row['Comments']
            date_str = row['Created_time'].strftime('%d %b %Y')

            # Build Tile HTML
            tile_html = f"""
            <div class="feedback-card {rating_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 0.85rem; letter-spacing: 0.5px;">{r.upper()}</span>
                    <span class="card-date">{date_str}</span>
                </div>
                <div class="feedback-text">
                    <div class="label">Reader Insight:</div>
                    "{comment}"
                </div>
            </div>
            """
            cols[col_index].markdown(tile_html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
