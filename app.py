import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# Custom CSS for total control over the layout
st.markdown("""
    <style>
    /* Global Container */
    .stats-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Individual Tile Style */
    .stat-tile {
        flex: 1;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #111;
    }

    /* Sentiment Bars Style */
    .bar-wrapper { margin-bottom: 10px; }
    .bar-container {
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 10px;
        height: 6px;
        overflow: hidden;
    }
    .bar-fill { height: 100%; border-radius: 10px; }
    .bar-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        margin-bottom: 3px;
        color: #444;
        font-weight: 700;
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
    .feedback-text { font-family: 'Georgia', serif; font-style: italic; color: #333; margin-top: 15px; font-size: 1.1rem; line-height: 1.6; }
    .label-sub { font-size: 0.7rem; color: #aaa; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px; }
    .card-date { color: #ccc; font-size: 0.75rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Gents Cafe Reader Feedback")

@st.cache_data
def load_data():
    file_name = "feedback.csv" 
    df = pd.read_csv(file_name)
    df.columns = ['Newsletter', 'Archive', 'Created_time', 'Email_Metadata', 'Email', 'Rating', 'Suggestions', 'Comments']
    df['Created_time'] = pd.to_datetime(df['Created_time'])
    return df

try:
    df = load_data()

    # --- TOP SELECTION MENU ---
    st.markdown("---")
    newsletter_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()
    
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        selected_issue = st.selectbox("Select a Newsletter Issue:", newsletter_list)
    st.markdown("---")

    issue_df = df[df['Newsletter'] == selected_issue]
    text_df = issue_df[issue_df['Comments'].notnull()].copy()

    # Calculations
    total_fb = len(issue_df)
    good_c = len(issue_df[issue_df['Rating'].str.contains('Good', case=False, na=False)])
    meh_c = len(issue_df[issue_df['Rating'].str.contains('Meh', case=False, na=False)])
    bad_c = len(issue_df[issue_df['Rating'].str.contains('bad', case=False, na=False)])
    
    good_p = (good_c / total_fb * 100) if total_fb > 0 else 0
    meh_p = (meh_c / total_fb * 100) if total_fb > 0 else 0
    bad_p = (bad_c / total_fb * 100) if total_fb > 0 else 0
    
    # --- TOP TILES ROW (PURE HTML) ---
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-tile">
            <div class="stat-label">Total Votes</div>
            <div class="stat-value">{total_fb}</div>
        </div>
        
        <div class="stat-tile">
            <div class="stat-label">Sentiment Breakdown</div>
            <div class="bar-wrapper">
                <div class="bar-info"><span>GOOD</span><span>{good_p:.1f}%</span></div>
                <div class="bar-container"><div class="bar-fill" style="width: {good_p}%; background-color: #2ecc71;"></div></div>
            </div>
            <div class="bar-wrapper">
                <div class="bar-info"><span>MEH</span><span>{meh_p:.1f}%</span></div>
                <div class="bar-container"><div class="bar-fill" style="width: {meh_p}%; background-color: #f1c40f;"></div></div>
            </div>
            <div class="bar-wrapper">
                <div class="bar-info"><span>BAD</span><span>{bad_p:.1f}%</span></div>
                <div class="bar-container"><div class="bar-fill" style="width: {bad_p}%; background-color: #e74c3c;"></div></div>
            </div>
        </div>
        
        <div class="stat-tile">
            <div class="stat-label">Comments to Read</div>
            <div class="stat-value">{len(text_df)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- TILES SECTION ---
    st.subheader(f"Direct Reader Comments: {selected_issue}")

    if len(text_df) == 0:
        st.info("No written comments found for this issue.")
    else:
        cols = st.columns(3)
        for i, (index, row) in enumerate(text_df.iterrows()):
            col_idx = i % 3
            r = str(row['Rating']).strip().capitalize()
            rating_cls = "rating-good" if "Good" in r else ("rating-meh" if "Meh" in r else "rating-bad")
            
            tile_html = f"""
            <div class="feedback-card {rating_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 0.85rem;">{r.upper()}</span>
                    <span class="card-date">{row['Created_time'].strftime('%d %b %Y')}</span>
                </div>
                <div class="feedback-text">
                    <div class="label-sub">Reader Insight:</div>
                    "{row['Comments']}"
                </div>
            </div>
            """
            cols[col_idx].markdown(tile_html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
