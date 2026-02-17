import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
    <style>
    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        height: 120px;
    }
    
    /* Sentiment Card Custom Style */
    .sentiment-card {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .sentiment-title {
        font-size: 0.8rem;
        color: rgb(49, 51, 63);
        margin-bottom: 8px;
    }
    
    .sentiment-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Pinterest Tiles */
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

    # Data filter
    issue_df = df[df['Newsletter'] == selected_issue]
    text_df = issue_df[issue_df['Comments'].notnull()].copy()

    # Calculation
    total_fb = len(issue_df)
    good_count = len(issue_df[issue_df['Rating'] == "Good"])
    sentiment_perc = (good_count / total_fb * 100) if total_fb > 0 else 0
    comments_shown = len(text_df)

    # --- TOP METRICS ROW ---
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Total Votes", total_fb)
        
    with m2:
        # Custom HTML Card for Sentiment with Progress Bar
        st.markdown(f"""
            <div class="sentiment-card">
                <div class="sentiment-title">Overall Sentiment (Good)</div>
                <div class="sentiment-value">{sentiment_perc:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
        # Progress bar immediately below the custom card text
        st.progress(sentiment_perc / 100)
        
    with m3:
        st.metric("Comments to Read", comments_shown)

    st.markdown("---")

    # --- PINTEREST TILES SECTION ---
    st.subheader(f"Direct Reader Comments: {selected_issue}")

    if comments_shown == 0:
        st.info("No written comments found for this issue (only ratings).")
    else:
        cols = st.columns(3)
        for i, (index, row) in enumerate(text_df.iterrows()):
            col_index = i % 3
            r = str(row['Rating']).strip()
            rating_class = "rating-good" if r == "Good" else ("rating-meh" if r == "Meh" else "rating-bad")
            comment = row['Comments']
            date_str = row['Created_time'].strftime('%d %b %Y')

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
