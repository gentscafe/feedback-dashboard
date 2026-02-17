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

    # --- PINTEREST TILES SECTION ---
    st.subheader(f"Detailed Feedback for: {selected_issue}")

    if written_count == 0:
        st.info("No detailed written feedback for this issue yet.")
    else:
        # Creating 3 columns for the Pinterest-like grid
        cols = st.columns(3)
        
        # We iterate through the rows and distribute them across columns
        for i, (index, row) in enumerate(text_df.iterrows()):
            col_index = i % 3  # This cycles through 0, 1, 2
            
            r = str(row['Rating']).strip()
            rating_class = "rating-good" if r == "Good" else ("rating-meh" if r == "Meh" else "rating-bad")
            
            comment = row['Comments'] if pd.notnull(row['Comments']) else ""
            suggestion = row['Suggestions'] if pd.notnull(row['Suggestions']) else ""
            date_str = row['Created_time'].strftime('%d %b %Y')

            # Building the Tile HTML
            tile_html = f"""
            <div class="feedback-card {rating_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 0.8rem;">{r.upper()}</span>
                    <span class="card-date">{date_str}</span>
                </div>
            """
            if comment:
                tile_html += f'<div class="feedback-text"><div class="label">Why they chose this:</div>"{comment}"</div>'
            if suggestion:
                tile_html += f'<div class="feedback-text"><div class="label">Suggestions:</div><div class="suggestion-text">{suggestion}</div></div>'
            
            tile_html += "</div>"
            
            # Place the tile in the correct column
            cols[col_index].markdown(tile_html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
