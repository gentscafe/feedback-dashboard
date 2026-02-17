import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Contributors Dashboard", layout="wide")

st.title("☕ Gents Cafe: Reader Feedback")
st.markdown("Select a newsletter issue below to see what readers had to say.")

# Data Loading
@st.cache_data
def load_data():
    file_name = "feedback.csv" 
    df = pd.read_csv(file_name)
    
    # Cleaning column names based on the specific CSV structure
    df.columns = [
        'Newsletter', 'Archive', 'Created_time', 'Email_Metadata', 'Email', 
        'Rating', 'Suggestions', 'Comments'
    ]
    
    # Convert date for sorting
    df['Created_time'] = pd.to_datetime(df['Created_time'])
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Contributor Access")
    
    # Get unique issues sorted by date (newest first)
    newsletter_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()
    
    selected_issue = st.sidebar.selectbox(
        "Which issue are you looking for?",
        newsletter_list
    )

    # Filtering data
    filtered_df = df[df['Newsletter'] == selected_issue]

    # --- RESULTS SECTION ---
    st.subheader(f"Feedback for: {selected_issue}")

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    total_fb = len(filtered_df)
    good_count = len(filtered_df[filtered_df['Rating'] == "Good"])
    comment_count = filtered_df['Comments'].dropna().count() + filtered_df['Suggestions'].dropna().count()
    
    col1.metric("Total Feedbacks", total_fb)
    col2.metric("Positive Ratings (Good)", good_count)
    col3.metric("Written Comments", int(comment_count))

    st.divider()

    # Detailed Feedback Table
    st.markdown("### 💬 Reader Comments & Suggestions")
    
    # Prepare display table
    display_df = filtered_df[['Rating', 'Suggestions', 'Comments']].copy()
    display_df.columns = ['Rating', 'How to improve?', 'Why they chose that rating']
    
    # Show table
    st.dataframe(
        display_df.fillna("-"), 
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Ensure the CSV file is uploaded to your GitHub repository and named 'feedback.csv'.")
