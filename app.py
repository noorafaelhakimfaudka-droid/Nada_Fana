import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity

# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Nada Fana | Musik Indie Mellow",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════
# CUSTOM CSS — PREMIUM DARK THEME
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Global Reset ── */
    .stApp {
        background: #050505;
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0a0a0a !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15); /* Subtle gold border */
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }

    /* ── Hero Header ── */
    .hero-container {
        background: linear-gradient(135deg, #111111 0%, #080808 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 4px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #d4af37; /* Gold */
        background: linear-gradient(135deg, #d4af37 0%, #fff8dc 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.02em;
        margin-bottom: 1rem;
        position: relative;
    }
    .hero-subtitle {
        color: #a0a0a0;
        font-size: 1.1rem;
        font-weight: 300;
        line-height: 1.8;
        position: relative;
        max-width: 800px;
        margin: 0 auto;
    }
    .hero-badge {
        display: inline-block;
        background: transparent;
        border: 1px solid rgba(212, 175, 55, 0.5);
        color: #d4af37;
        padding: 0.4rem 1.2rem;
        border-radius: 2px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    /* ── Metric Cards ── */
    .metric-row {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        flex: 1;
        background: #0d0d0d;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(212, 175, 55, 0.3);
        background: #111111;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 400;
        color: #ffffff;
    }
    .metric-label {
        color: #7a7a7a;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 0.5rem;
    }

    /* ── Song Cards ── */
    .song-card {
        background: #0d0d0d;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
    }
    .song-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 2px;
        height: 100%;
        background: #d4af37;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .song-card:hover {
        border-color: rgba(212, 175, 55, 0.2);
        background: #111111;
        transform: translateX(4px);
    }
    .song-card:hover::before {
        opacity: 1;
    }
    .song-rank {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 400;
        color: #ffffff;
        margin-right: 1.5rem;
        min-width: 40px;
        text-align: right;
    }
    .song-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    .song-artist {
        color: #a0a0a0;
        font-size: 0.9rem;
        font-weight: 400;
        letter-spacing: 0.05em;
    }
    .song-score {
        font-family: 'Inter', sans-serif;
        background: transparent;
        border: 1px solid rgba(212, 175, 55, 0.3);
        color: #d4af37;
        padding: 0.4rem 1rem;
        border-radius: 2px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.1em;
    }

    /* ── Reference Card ── */
    .ref-card {
        background: #0a0a0a;
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 4px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .ref-label {
        color: #d4af37;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 1rem;
    }
    .ref-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .ref-artist {
        font-size: 1.1rem;
        font-weight: 300;
        color: #a0a0a0;
        letter-spacing: 0.05em;
    }

    /* ── Section Headers ── */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
    }

    /* ── Audio Feature Bars ── */
    .feature-bar-container {
        margin-bottom: 1.2rem;
    }
    .feature-bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }
    .feature-bar-name {
        color: #a0a0a0;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .feature-bar-value {
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 400;
    }
    .feature-bar-track {
        background: #1a1a1a;
        height: 4px;
        overflow: hidden;
    }
    .feature-bar-fill {
        height: 100%;
        background: #d4af37;
        transition: width 0.8s ease;
    }

    /* ── Lyric Box ── */
    .lyric-box {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 2rem;
        max-height: 400px;
        overflow-y: auto;
        color: #cccccc;
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        line-height: 2;
        font-style: italic;
        text-align: center;
    }
    .lyric-box::-webkit-scrollbar {
        width: 4px;
    }
    .lyric-box::-webkit-scrollbar-track {
        background: transparent;
    }
    .lyric-box::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #7a7a7a;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 1rem 0;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        border-bottom: 2px solid #d4af37 !important;
        color: #ffffff !important;
    }

    /* ── Streamlit Element Overrides ── */
    .stSelectbox label, .stSlider label, .stTextInput label {
        color: #a0a0a0 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif;
    }

    /* ── Hide streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Plotly chart backgrounds ── */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }
    /* ── UI Fixes ── */
    /* Menyembunyikan tombol fullscreen bawaan pada chart */
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* Menyembunyikan tombol fullscreen bawaan pada chart */
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* BULLETPROOF: Memastikan tombol sidebar & header selalu terlihat */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    header[data-testid="stHeader"] svg {
        fill: #d4af37 !important;
        stroke: #d4af37 !important;
    }
    [data-testid="collapsedControl"] {
        background-color: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid #d4af37 !important;
        border-radius: 4px !important;
        margin: 10px !important;
        z-index: 999999 !important;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# DATA LOADING (CACHED)
# ══════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    """Memuat database lagu dan matriks embedding dari file pickle."""
    df = pickle.load(open('database_lagu.pkl', 'rb'))
    embeddings = pickle.load(open('memori_ai.pkl', 'rb'))
    return df, embeddings

df, embeddings = load_data()

# Pre-compute daftar artis unik (sorted)
daftar_artis = sorted(df['artists'].unique().tolist())


# ══════════════════════════════════════════════════════════════════════
# RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════════
def get_recommendations(index, jumlah=5):
    """Menghitung cosine similarity dan mengembalikan top-N rekomendasi."""
    sim_scores = cosine_similarity(
        embeddings[index].reshape(1, -1),
        embeddings
    ).flatten()

    # Sort descending, skip dirinya sendiri
    top_indices = np.argsort(sim_scores)[::-1]
    results = []
    for idx in top_indices:
        if idx != index:
            results.append({
                'index': idx,
                'name': df.iloc[idx]['name'],
                'artists': df.iloc[idx]['artists'],
                'score': sim_scores[idx],
                'valence': df.iloc[idx]['valence'],
                'acousticness': df.iloc[idx]['acousticness'],
                'energy': df.iloc[idx]['energy'],
                'danceability': df.iloc[idx]['danceability'],
                'tempo': df.iloc[idx].get('tempo', 0),
            })
            if len(results) >= jumlah:
                break
    return results


def render_feature_bar(name, value, color_start, color_end):
    """Membuat HTML bar fitur audio kustom."""
    pct = value * 100
    return f"""
    <div class="feature-bar-container">
        <div class="feature-bar-label">
            <span class="feature-bar-name">{name}</span>
            <span class="feature-bar-value">{value:.3f}</span>
        </div>
        <div class="feature-bar-track">
            <div class="feature-bar-fill" style="width: {pct}%; background: linear-gradient(90deg, {color_start}, {color_end});"></div>
        </div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Nada Fana</div>
    <div class="hero-subtitle">
        Mesin rekomendasi musik cerdas yang mengkurasi lagu-lagu <em>mellow</em> & akustik
        berdasarkan kedalaman makna lirik menggunakan <strong>TF-IDF</strong>
        dan <strong>Cosine Similarity</strong>.
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# STATS METRICS ROW
# ══════════════════════════════════════════════════════════════════════
total_lagu = len(df)
total_artis = df['artists'].nunique()
avg_acousticness = df['acousticness'].mean()
avg_valence = df['valence'].mean()

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{total_lagu:,}</div>
        <div class="metric-label">Total Lagu Mellow</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{total_artis}</div>
        <div class="metric-label">Artis Unik</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{avg_acousticness:.2f}</div>
        <div class="metric-label">Rerata Akustik</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{avg_valence:.2f}</div>
        <div class="metric-label">Rerata Emosi</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR — SEARCH CONTROLS
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span style="font-size: 2.5rem;"></span>
        <h2 style="color: #e6edf3; margin: 0.5rem 0 0.2rem; font-weight: 800;">Cari Lagu</h2>
        <p style="color: #a0a0a0; font-size: 0.85rem;">Temukan rekomendasi mellow untukmu</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Mode pencarian
    mode = st.radio(
        " Mode Pencarian",
        ["Cari Artis", "Cari Judul Lagu", "Jelajahi Semua"],
        index=0,
    )

    selected_index = None

    if mode == "Cari Artis":
        artis_input = st.selectbox(
            " Pilih Artis",
            options=[""] + daftar_artis,
            index=0,
            placeholder="Ketik nama artis...",
        )
        if artis_input:
            lagu_artis = df[df['artists'] == artis_input][['name', 'artists']].reset_index()
            if not lagu_artis.empty:
                pilihan_lagu = st.selectbox(
                    " Pilih Lagu",
                    options=lagu_artis['name'].tolist(),
                    index=0,
                )
                selected_index = int(lagu_artis[lagu_artis['name'] == pilihan_lagu]['index'].values[0])
            else:
                st.warning("Artis tidak ditemukan.")

    elif mode == "Cari Judul Lagu":
        judul_input = st.text_input(" Ketik judul lagu", placeholder="contoh: Tutur Batin")
        if judul_input:
            hasil = df[df['name'].str.contains(judul_input, case=False, na=False)][['name', 'artists']].reset_index()
            if not hasil.empty:
                pilihan = st.selectbox(
                    "Hasil pencarian:",
                    options=[f"{r['name']} — {r['artists']}" for _, r in hasil.iterrows()],
                    index=0,
                )
                for _, r in hasil.iterrows():
                    if f"{r['name']} — {r['artists']}" == pilihan:
                        selected_index = int(r['index'])
                        break
            else:
                st.warning("Lagu tidak ditemukan. Coba kata kunci lain.")

    elif mode == "Jelajahi Semua":
        sample_df = df.sample(20, random_state=42)[['name', 'artists']].reset_index()
        pilihan = st.selectbox(
            " Lagu Acak (20 sampel)",
            options=[f"{r['name']} — {r['artists']}" for _, r in sample_df.iterrows()],
            index=0,
        )
        for _, r in sample_df.iterrows():
            if f"{r['name']} — {r['artists']}" == pilihan:
                selected_index = int(r['index'])
                break

    st.markdown("---")

    jumlah_rekomendasi = st.slider(
        " Jumlah Rekomendasi",
        min_value=3,
        max_value=15,
        value=5,
        step=1
    )

    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 12px; padding: 1rem; margin-top: 0.5rem;">
        <p style="color: #d4af37; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;"> Cara Kerja</p>
        <p style="color: #a0a0a0; font-size: 0.75rem; line-height: 1.5; margin: 0;">
            Setiap lirik dikonversi menjadi matriks fitur oleh algoritma <strong style="color: #ffffff;">TF-IDF (Term Frequency-Inverse Document Frequency)</strong>,
            lalu <strong style="color: #ffffff;">Cosine Similarity</strong> mengukur kedekatan makna antar lagu.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════
if selected_index is not None:
    ref_song = df.iloc[selected_index]
    recommendations = get_recommendations(selected_index, jumlah_rekomendasi)

    # ── Reference Song Card ──
    st.markdown(f"""
    <div class="ref-card">
        <div class="ref-label"> Lagu Referensi</div>
        <div class="ref-title">{ref_song['name']}</div>
        <div class="ref-artist">oleh {ref_song['artists']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two Column Layout ──
    col_recs, col_details = st.columns([3, 2], gap="large")

    with col_recs:
        st.markdown('<div class="section-header"><span class="section-icon"></span>Rekomendasi AI</div>', unsafe_allow_html=True)

        for i, rec in enumerate(recommendations, 1):
            score_pct = rec['score'] * 100
            st.markdown(f"""
            <div class="song-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span class="song-rank">{i:02d}</span>
                        <div>
                            <div class="song-title">{rec['name']}</div>
                            <div class="song-artist">{rec['artists']}</div>
                        </div>
                    </div>
                    <span class="song-score"> {score_pct:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_details:
        st.markdown('<div class="section-header"><span class="section-icon"></span>DNA Audio Referensi</div>', unsafe_allow_html=True)

        # Feature bars
        features_html = ""
        features_html += render_feature_bar(" Valence (Emosi)", ref_song['valence'], "#d4af37", "#bf953f")
        features_html += render_feature_bar(" Akustik", ref_song['acousticness'], "#e5e4e2", "#c0c0c0")
        features_html += render_feature_bar(" Energi", ref_song['energy'], "#d4af37", "#996515")
        features_html += render_feature_bar(" Dansa", ref_song['danceability'], "#f3e5ab", "#d4af37")
        if 'tempo' in ref_song and ref_song['tempo'] > 0:
            tempo_normalized = min(ref_song['tempo'] / 200, 1.0)
            features_html += render_feature_bar(f" Tempo ({ref_song['tempo']:.0f} BPM)", tempo_normalized, "#e5e4e2", "#b0b0b0")
        st.markdown(features_html, unsafe_allow_html=True)

        # Lyric preview
        if 'lyrics' in ref_song and pd.notna(ref_song['lyrics']):
            st.markdown('<div class="section-header" style="margin-top: 1.5rem;"><span class="section-icon"></span>Kutipan Lirik</div>', unsafe_allow_html=True)
            lirik_preview = str(ref_song['lyrics'])[:500].replace('\n', '<br>')
            st.markdown(f'<div class="lyric-box">{lirik_preview}...</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # VISUALIZATIONS
    # ══════════════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)

    tab_radar, tab_scatter, tab_compare = st.tabs([
        " Radar Perbandingan",
        " Peta Audio",
        " Tabel Lengkap"
    ])

    # Warna plotly yang selaras dengan theme
    plot_bg = 'rgba(10, 10, 15, 0)'
    paper_bg = 'rgba(10, 10, 15, 0)'
    grid_color = 'rgba(212, 175, 55, 0.05)'
    text_color = '#a0a0a0'

    with tab_radar:
        categories = ['Valence (Emosi)', 'Akustik', 'Energi', 'Dansa']

        fig_radar = go.Figure()

        # Reference song
        ref_vals = [ref_song['valence'], ref_song['acousticness'], ref_song['energy'], ref_song['danceability']]
        fig_radar.add_trace(go.Scatterpolar(
            r=ref_vals + [ref_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(212, 175, 55, 0.15)',
            line=dict(color='#d4af37', width=2.5),
            name=f" {ref_song['name'][:25]}",
        ))

        # Top 3 recommendations
        colors = ['#e5e4e2', '#d4af37', '#f3e5ab']
        for i, rec in enumerate(recommendations[:3]):
            vals = [rec['valence'], rec['acousticness'], rec['energy'], rec['danceability']]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=f'rgba({int(colors[i][1:3], 16)}, {int(colors[i][3:5], 16)}, {int(colors[i][5:7], 16)}, 0.05)',
                line=dict(color=colors[i], width=1.5, dash='dot'),
                name=f"#{i+1} {rec['name'][:25]}",
            ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor=plot_bg,
                radialaxis=dict(visible=True, range=[0, 1], gridcolor=grid_color, tickfont=dict(color=text_color, size=10)),
                angularaxis=dict(gridcolor=grid_color, tickfont=dict(color='#ffffff', size=12)),
            ),
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            showlegend=True,
            legend=dict(font=dict(color=text_color, size=11), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=80, r=80, t=40, b=40),
            height=450,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with tab_scatter:
        scatter_data = []
        scatter_data.append({
            'name': ref_song['name'],
            'artists': ref_song['artists'],
            'valence': ref_song['valence'],
            'energy': ref_song['energy'],
            'acousticness': ref_song['acousticness'],
            'danceability': ref_song['danceability'],
            'tipe': ' Referensi',
            'size': 18,
        })
        for i, rec in enumerate(recommendations, 1):
            scatter_data.append({
                'name': rec['name'],
                'artists': rec['artists'],
                'valence': rec['valence'],
                'energy': rec['energy'],
                'acousticness': rec['acousticness'],
                'danceability': rec['danceability'],
                'tipe': f'Rekomendasi #{i}',
                'size': 12,
            })

        scatter_df = pd.DataFrame(scatter_data)

        fig_scatter = px.scatter(
            scatter_df,
            x='valence',
            y='energy',
            size='size',
            color='tipe',
            hover_data=['name', 'artists', 'acousticness', 'danceability'],
            color_discrete_sequence=['#d4af37', '#e5e4e2', '#f3e5ab', '#d4af37', '#e5e4e2', '#34d399'] + ['#64748b'] * 15,
            labels={'valence': 'Valence (Emosi →)', 'energy': 'Energi (Intensitas →)'},
        )
        fig_scatter.update_layout(
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            xaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff'), range=[0, 1]),
            yaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff'), range=[0, 1]),
            legend=dict(font=dict(color=text_color, size=11), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=60, r=40, t=40, b=60),
            height=450,
        )

        # Quadrant annotations
        fig_scatter.add_annotation(x=0.15, y=0.95, text=" Intens & Sedih", showarrow=False, font=dict(color='rgba(139,148,158,0.4)', size=11))
        fig_scatter.add_annotation(x=0.85, y=0.95, text=" Intens & Ceria", showarrow=False, font=dict(color='rgba(139,148,158,0.4)', size=11))
        fig_scatter.add_annotation(x=0.15, y=0.05, text=" Mellow & Sendu", showarrow=False, font=dict(color='rgba(139,148,158,0.4)', size=11))
        fig_scatter.add_annotation(x=0.85, y=0.05, text=" Santai & Bahagia", showarrow=False, font=dict(color='rgba(139,148,158,0.4)', size=11))

        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

    with tab_compare:
        table_data = []
        table_data.append({
            '#': '',
            'Judul': ref_song['name'],
            'Artis': ref_song['artists'],
            'Valence': f"{ref_song['valence']:.3f}",
            'Akustik': f"{ref_song['acousticness']:.3f}",
            'Energi': f"{ref_song['energy']:.3f}",
            'Dansa': f"{ref_song['danceability']:.3f}",
            'Skor Kemiripan': '—',
        })
        for i, rec in enumerate(recommendations, 1):
            table_data.append({
                '#': str(i),
                'Judul': rec['name'],
                'Artis': rec['artists'],
                'Valence': f"{rec['valence']:.3f}",
                'Akustik': f"{rec['acousticness']:.3f}",
                'Energi': f"{rec['energy']:.3f}",
                'Dansa': f"{rec['danceability']:.3f}",
                'Skor Kemiripan': f"{rec['score']:.4f}",
            })

        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True,
            hide_index=True,
        )

else:
    # ══════════════════════════════════════════════════════════════════
    # EMPTY STATE — EXPLORE MODE
    # ══════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem;">
        <span style="font-size: 4rem; display: block; margin-bottom: 1rem;"></span>
        <h2 style="color: #e6edf3; font-weight: 800; margin-bottom: 0.5rem;">Mulai Jelajahi</h2>
        <p style="color: #a0a0a0; font-size: 1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
            Pilih artis atau judul lagu dari panel samping untuk mendapatkan rekomendasi
            lagu <em>mellow</em> yang mirip secara makna lirik.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Warna plotly yang selaras dengan theme
    plot_bg = 'rgba(10, 10, 15, 0)'
    paper_bg = 'rgba(10, 10, 15, 0)'
    grid_color = 'rgba(212, 175, 55, 0.05)'
    text_color = '#a0a0a0'

    # Show a sample distribution chart
    st.markdown('<div class="section-header"><span class="section-icon"></span>Distribusi Fitur Audio Dataset</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            df, x='valence', nbins=40,
            color_discrete_sequence=['#d4af37'],
            labels={'valence': 'Valence (Skor Emosi)', 'count': 'Jumlah'},
            opacity=0.8,
        )
        fig_hist.update_layout(
            paper_bgcolor=paper_bg, plot_bgcolor=plot_bg,
            xaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff')),
            yaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff')),
            margin=dict(l=40, r=20, t=30, b=40), height=300,
            title=dict(text="Distribusi Valence (Emosi)", font=dict(color='#ffffff', size=14)),
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig_hist2 = px.histogram(
            df, x='acousticness', nbins=40,
            color_discrete_sequence=['#e5e4e2'],
            labels={'acousticness': 'Skor Akustik', 'count': 'Jumlah'},
            opacity=0.8,
        )
        fig_hist2.update_layout(
            paper_bgcolor=paper_bg, plot_bgcolor=plot_bg,
            xaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff')),
            yaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff')),
            margin=dict(l=40, r=20, t=30, b=40), height=300,
            title=dict(text="Distribusi Akustik", font=dict(color='#ffffff', size=14)),
        )
        st.plotly_chart(fig_hist2, use_container_width=True, config={'displayModeBar': False})

    # Artist top chart
    st.markdown('<div class="section-header"><span class="section-icon">🏆</span>15 Artis Teratas</div>', unsafe_allow_html=True)

    top_artists = df['artists'].value_counts().head(15).reset_index()
    top_artists.columns = ['Artis', 'Jumlah Lagu']

    fig_bar = px.bar(
        top_artists,
        x='Jumlah Lagu',
        y='Artis',
        orientation='h',
        color='Jumlah Lagu',
        color_continuous_scale=['#312e81', '#4338ca', '#bf953f', '#d4af37', '#d4af37'],
    )
    fig_bar.update_layout(
        paper_bgcolor=paper_bg, plot_bgcolor=plot_bg,
        xaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color), title_font=dict(color='#ffffff')),
        yaxis=dict(tickfont=dict(color='#ffffff', size=11), title_font=dict(color='#ffffff'), autorange='reversed'),
        margin=dict(l=10, r=20, t=20, b=40), height=420,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
