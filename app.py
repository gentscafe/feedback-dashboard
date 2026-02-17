import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# CSS "Scored" - Robusto e pulito
st.markdown("""
    <style>
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .metric-title { font-size: 0.75rem; color: #888; text-transform: uppercase; font-weight: 700; margin-bottom: 10px; }
    .metric-value { font-size: 2.5rem; font-weight: 700; color: #111; }
    .bar-item { margin-bottom: 8px; text-align: left; }
    .bar-header { display: flex; justify-content: space-between; font-size: 0.7rem; font-weight: 700; margin-bottom: 2px; }
    .bar-bg { width: 100%; background-color: #f0f0f0; height: 6px; border-radius: 10px; }
    .bar-fill { height: 100%; border-radius: 10px; }
    .feedback-card { background-color: #ffffff; border-radius: 12px; padding: 22px; margin-bottom: 20px; border-top: 6px solid #333; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .rating-good { border-top-color: #2ecc71; }
    .rating-meh { border-top-color: #f1c40f; }
    .rating-bad { border-top-color: #e74c3c; }
    .quote { font-family: 'Georgia', serif; font-style: italic; color: #333; font-size: 1.1rem; line-height: 1.6; margin-top: 10px; }
    .insight-label { font-size: 0.65rem; color: #aaa; text-transform: uppercase; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Gents Cafe Reader Feedback")

@st.cache_data
def load_data():
    file_name = "feedback.csv" 
    df = pd.read_csv(file_name)
    # Assicurati che la colonna con i titoli degli articoli si chiami 'Article Title' nel CSV
    # Se ha un altro nome, cambialo qui sotto nell'elenco
    df.columns = ['Newsletter', 'Archive', 'Created_time', 'Email_Metadata', 'Email', 'Rating', 'Suggestions', 'Comments', 'Article_Title']
    df['Created_time'] = pd.to_datetime(df['Created_time'])
    return df

try:
    df = load_data()

    st.markdown("---")
    
    # --- SEZIONE RICERCA DOPPIA ---
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        # Ricerca per Titolo Articolo
        all_articles = sorted(df['Article_Title'].dropna().unique().tolist())
        selected_article = st.selectbox("Search by Article Title:", ["-- Select Article --"] + all_articles)

    with col_search2:
        # Se un articolo è selezionato, pre-selezioniamo la newsletter corrispondente
        if selected_article != "-- Select Article --":
            default_issue = df[df['Article_Title'] == selected_article]['Newsletter'].iloc[0]
            issue_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()
            # Troviamo l'indice della newsletter corretta
            default_index = issue_list.index(default_issue)
            selected_issue = st.selectbox("Newsletter Issue:", issue_list, index=default_index)
        else:
            issue_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()
            selected_issue = st.selectbox("Or select by Issue Number:", issue_list)

    st.markdown("---")

    # Filtri Dati
    issue_df = df[df['Newsletter'] == selected_issue]
    text_df = issue_df[issue_df['Comments'].notnull()].copy()

    # Calcoli Sentiment
    total = len(issue_df)
    def get_count(label):
        return len(issue_df[issue_df['Rating'].str.contains(label, case=False, na=False)])
    
    g_c, m_c, b_c = get_count('Good'), get_count('Meh'), get_count('bad')
    g_p = (g_c/total*100) if total > 0 else 0
    m_p = (m_c/total*100) if total > 0 else 0
    b_p = (b_c/total*100) if total > 0 else 0

    # --- TOP ROW (STATISTICHE) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-title">Total Votes</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Sentiment</div>
            <div class="bar-item">
                <div class="bar-header"><span>GOOD</span><span>{g_p:.1f}%</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:{g_p}%; background-color:#2ecc71;"></div></div>
            </div>
            <div class="bar-item">
                <div class="bar-header"><span>MEH</span><span>{m_p:.1f}%</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:{m_p}%; background-color:#f1c40f;"></div></div>
            </div>
            <div class="bar-item">
                <div class="bar-header"><span>BAD</span><span>{b_p:.1f}%</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:{b_p}%; background-color:#e74c3c;"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-title">Comments</div><div class="metric-value">{len(text_df)}</div></div>', unsafe_allow_html=True)

    # --- TILES ---
    st.subheader(f"Comments for: {selected_issue}")
    
    # Mostriamo quali articoli sono contenuti in questa newsletter (per conferma)
    current_articles = issue_df['Article_Title'].dropna().unique().tolist()
    if current_articles:
        st.caption(f"Articles in this issue: {', '.join(current_articles)}")

    if len(text_df) == 0:
        st.info("No comments for this issue.")
    else:
        t_cols = st.columns(3)
        for i, (idx, row) in enumerate(text_df.iterrows()):
            r_str = str(row['Rating']).strip().capitalize()
            cls = "rating-good" if "Good" in r_str else ("rating-meh" if "Meh" in r_str else "rating-bad")
            tile = f"""
            <div class="feedback-card {cls}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-weight:800; font-size:0.7rem;">{r_str.upper()}</span>
                    <span style="color:#ccc; font-size:0.7rem;">{row['Created_time'].strftime('%d %b %Y')}</span>
                </div>
                <div class="insight-label">Reader Insight:</div>
                <div class="quote">"{row['Comments']}"</div>
            </div>
            """
            t_cols[i % 3].markdown(tile, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
