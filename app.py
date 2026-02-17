import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Gents Cafe Reader Feedback", layout="wide")

# CSS per il design delle card e delle statistiche
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
    # Carichiamo il file con i nomi colonne originali del tuo CSV
    df = pd.read_csv(file_name)
    
    # Rinominiamo solo le colonne che ci servono per comodità nel codice
    df = df.rename(columns={
        'Newsletter': 'Newsletter',
        'Created time': 'Created_time',
        'Essays': 'Article_Title',
        "How did you like this week's issue?": 'Rating',
        "While you're here, do you mind telling us why you chose that? (optional)": 'Comments'
    })
    
    # Convertiamo la data in un formato leggibile
    df['Created_time'] = pd.to_datetime(df['Created_time'], errors='coerce')
    return df

try:
    df = load_data()

    st.markdown("---")
    
    # --- SEZIONE DI RICERCA ---
    col_search1, col_search2 = st.columns(2)
    
    # Prepariamo le liste per i menu a tendina
    # Prendiamo i titoli unici dalla colonna Essays (Article_Title)
    all_articles = sorted(df['Article_Title'].dropna().unique().tolist())
    # Prendiamo le newsletter uniche
    issue_list = df.sort_values('Created_time', ascending=False)['Newsletter'].unique().tolist()

    with col_search1:
        selected_article = st.selectbox("Cerca per Titolo Articolo:", ["-- Seleziona Articolo --"] + all_articles)

    with col_search2:
        if selected_article != "-- Seleziona Articolo --":
            # Trova la newsletter associata all'articolo scelto
            matching_issue = df[df['Article_Title'] == selected_article]['Newsletter'].iloc[0]
            try:
                idx = issue_list.index(matching_issue)
                selected_issue = st.selectbox("Newsletter associata:", issue_list, index=idx)
            except:
                selected_issue = st.selectbox("Seleziona Newsletter:", issue_list)
        else:
            selected_issue = st.selectbox("Oppure seleziona per Numero Issue:", issue_list)

    st.markdown("---")

    # Filtriamo i dati per la newsletter selezionata
    issue_df = df[df['Newsletter'] == selected_issue]
    # Filtriamo solo i feedback che hanno un commento scritto
    text_df = issue_df[issue_df['Comments'].notnull()].copy()

    # Calcoli per il Sentiment
    total = len(issue_df)
    def get_count(label):
        return len(issue_df[issue_df['Rating'].astype(str).str.contains(label, case=False, na=False)])
    
    g_c, m_c, b_c = get_count('Good'), get_count('Meh'), get_count('bad')
    g_p = (g_c/total*100) if total > 0 else 0
    m_p = (m_c/total*100) if total > 0 else 0
    b_p = (b_c/total*100) if total > 0 else 0

    # --- RIGA SUPERIORE: STATISTICHE ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-title">Voti Totali</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
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
        st.markdown(f'<div class="metric-box"><div class="metric-title">Commenti</div><div class="metric-value">{len(text_df)}</div></div>', unsafe_allow_html=True)

    # --- SEZIONE FEEDBACK (TILE) ---
    st.subheader(f"Commenti per: {selected_issue}")
    
    # Mostriamo quali articoli sono presenti in questa newsletter
    current_articles = issue_df['Article_Title'].dropna().unique().tolist()
    if current_articles:
        st.caption(f"Articoli in questa edizione: {', '.join(current_articles)}")

    if len(text_df) == 0:
        st.info("Nessun commento scritto per questa edizione (solo voti).")
    else:
        t_cols = st.columns(3)
        for i, (idx, row) in enumerate(text_df.iterrows()):
            r_str = str(row['Rating']).strip().capitalize()
            # Identifichiamo il colore in base al rating
            if "Good" in r_str: cls = "rating-good"
            elif "Meh" in r_str: cls = "rating-meh"
            else: cls = "rating-bad"
            
            tile = f"""
            <div class="feedback-card {cls}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-weight:800; font-size:0.7rem;">{r_str.upper()}</span>
                    <span style="color:#ccc; font-size:0.7rem;">{row['Created_time'].strftime('%d %b %Y') if pd.notnull(row['Created_time']) else ''}</span>
                </div>
                <div class="insight-label">Feedback del lettore:</div>
                <div class="quote">"{row['Comments']}"</div>
            </div>
            """
            t_cols[i % 3].markdown(tile, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Si è verificato un errore: {e}")
