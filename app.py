import streamlit as st
import numpy as np
from PIL import Image
from modules.input_gambar import load_gambar, tampilkan_gambar, get_info_gambar
from modules.grayscale_biner import konversi_grayscale, konversi_biner, konversi_biner_otsu
from modules.aritmatika_logika import (operasi_penjumlahan, operasi_pengurangan,
                                        operasi_perkalian, operasi_pembagian,
                                        operasi_and, operasi_or,
                                        operasi_not, operasi_xor)
from modules.histogram import tampilkan_histogram
from modules.konvolusi import filter_mean, filter_sharpening, filter_sobel, filter_prewitt
from modules.morfologi import erosi, dilasi, opening, closing

# ── Konfigurasi halaman ──────────────────────────────────────────
st.set_page_config(
    page_title="Pengolahan Citra Digital",
    page_icon="✦",
    layout="wide"
)

# ╔══════════════════════════════════════════════════════════════════╗
# ║          REDESIGN CSS — SOFT PASTEL ELEGANT AESTHETIC           ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Manrope:wght@400;500;600;700;800&display=swap');

/* ── Design Tokens ────────────────────────────────────────────── */
:root {
    --primary:       #C8A2FF;
    --primary-deep:  #A97CF8;
    --secondary:     #F3D4FF;
    --accent:        #FFD6CC;
    --accent-warm:   #FFBFA8;
    --bg:            #FFFDFE;
    --surface:       #FFFFFF;
    --surface-tint:  #FBF7FF;
    --text:          #3B3650;
    --text-muted:    #7B7690;
    --text-light:    #ADA8C0;
    --border:        #EEEAF7;
    --border-soft:   #F5F0FF;
    --lavender-soft: rgba(200,162,255,.10);
    --lavender-mid:  rgba(200,162,255,.18);
    --peach-soft:    rgba(255,214,204,.18);
    --shadow-xs:     0 1px 4px rgba(163,124,248,.06);
    --shadow-sm:     0 2px 12px rgba(163,124,248,.10);
    --shadow-md:     0 6px 28px rgba(163,124,248,.14);
    --shadow-lg:     0 12px 48px rgba(163,124,248,.18);
    --radius:        18px;
    --radius-lg:     24px;
    --radius-xl:     32px;
    --radius-pill:   999px;
}

/* ── Reset & Base ─────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
    font-family: 'Poppins', 'Manrope', system-ui, sans-serif !important;
    color: var(--text) !important;
}

/* ── App Background — soft mesh gradient ─────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(243,212,255,.30) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 10%, rgba(255,214,204,.28) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 100%, rgba(200,162,255,.14) 0%, transparent 60%),
        #FFFDFE !important;
    background-attachment: fixed !important;
}

/* ── Hide Streamlit chrome ────────────────────────────────────── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }

/* ── Main container ───────────────────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1180px;
}

/* ══════════════════════════════════════════════════════════════
   SIDEBAR — Pastel Elegant
══════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #FBF7FF 0%,
        #F8F2FF 40%,
        #FFF5F3 80%,
        #FBF7FF 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 20px rgba(200,162,255,.08) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] .block-container { padding: 0 1rem 1.5rem !important; }

/* Sidebar text */
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,.85) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    box-shadow: var(--shadow-xs) !important;
    transition: all .25s ease;
    backdrop-filter: blur(8px);
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(200,162,255,.15) !important;
}

/* Sidebar file uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(200,162,255,.06) !important;
    border: 1.5px dashed rgba(200,162,255,.45) !important;
    border-radius: var(--radius) !important;
    transition: all .25s ease;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: var(--primary) !important;
    background: rgba(200,162,255,.10) !important;
}

[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 0.5rem 0 !important;
}

/* ══════════════════════════════════════════════════════════════
   SIDEBAR LOGO AREA
══════════════════════════════════════════════════════════════ */
.sb-logo {
    text-align: center;
    padding: 1.8rem 1rem 1.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    background: linear-gradient(135deg, rgba(200,162,255,.08), rgba(255,214,204,.06));
}
.sb-logo-mark {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, var(--primary), var(--accent-warm));
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; margin: 0 auto 10px;
    box-shadow: 0 4px 16px rgba(200,162,255,.35);
}
.sb-logo-name {
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    letter-spacing: .3px;
    display: block;
}
.sb-logo-sub {
    font-size: 0.68rem !important;
    color: var(--text-light) !important;
    display: block;
    margin-top: 2px;
    font-weight: 400 !important;
}
.sb-section-label {
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--text-light) !important;
    padding: 0.6rem 0 0.3rem;
    display: block;
}
.sb-upload-note {
    font-size: 0.7rem !important;
    color: var(--text-light) !important;
    text-align: center;
    margin-top: 4px !important;
}

/* ══════════════════════════════════════════════════════════════
   HERO / APP HEADER
══════════════════════════════════════════════════════════════ */
.hero {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 2rem;
    align-items: center;
    padding: 2.5rem 2.8rem;
    background: linear-gradient(135deg,
        rgba(200,162,255,.12) 0%,
        rgba(243,212,255,.08) 50%,
        rgba(255,214,204,.10) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}
.hero::before {
    content: "";
    position: absolute;
    top: -80px; right: -80px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(200,162,255,.20), transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -60px; left: 10%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,214,204,.22), transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--primary-deep);
    background: rgba(200,162,255,.15);
    border: 1px solid rgba(200,162,255,.30);
    border-radius: var(--radius-pill);
    padding: 4px 14px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Manrope', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    line-height: 1.2 !important;
    margin: 0 0 .5rem !important;
    letter-spacing: -0.5px;
}
.hero h1 em {
    font-style: italic;
    background: linear-gradient(135deg, var(--primary-deep), var(--accent-warm));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 420px;
    margin-bottom: 1.4rem;
}
.hero-cta-row { display: flex; gap: 10px; flex-wrap: wrap; }
.btn-primary {
    display: inline-flex; align-items: center; gap: 7px;
    background: linear-gradient(135deg, var(--primary), var(--primary-deep));
    color: white !important;
    font-size: 0.83rem; font-weight: 600;
    padding: 10px 22px;
    border-radius: var(--radius-pill);
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(200,162,255,.40);
    transition: all .25s ease;
    border: none; cursor: pointer;
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(200,162,255,.50);
}
.btn-ghost {
    display: inline-flex; align-items: center; gap: 7px;
    background: white;
    color: var(--text) !important;
    font-size: 0.83rem; font-weight: 500;
    padding: 10px 22px;
    border-radius: var(--radius-pill);
    text-decoration: none;
    border: 1.5px solid var(--border);
    transition: all .25s ease;
    cursor: pointer;
}
.btn-ghost:hover {
    border-color: var(--primary);
    color: var(--primary-deep) !important;
    background: rgba(200,162,255,.06);
}
.hero-orb {
    width: 160px; height: 160px;
    background: linear-gradient(135deg,
        rgba(200,162,255,.25),
        rgba(255,214,204,.30),
        rgba(243,212,255,.20));
    border-radius: 40% 60% 55% 45% / 45% 40% 60% 55%;
    border: 1px solid rgba(200,162,255,.30);
    backdrop-filter: blur(20px);
    display: flex; align-items: center; justify-content: center;
    font-size: 4rem;
    animation: float 6s ease-in-out infinite;
    flex-shrink: 0;
    position: relative; z-index: 1;
    box-shadow: 0 8px 32px rgba(200,162,255,.20);
}
@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    33%       { transform: translateY(-8px) rotate(2deg); }
    66%       { transform: translateY(-4px) rotate(-1deg); }
}
.hero-stats {
    display: flex; gap: 2rem;
    margin-top: 1.4rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--border-soft);
}
.hero-stat-num {
    font-family: 'Manrope', sans-serif;
    font-size: 1.5rem; font-weight: 800;
    color: var(--primary-deep);
    line-height: 1;
}
.hero-stat-label {
    font-size: 0.7rem;
    color: var(--text-light);
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: .5px;
    font-weight: 500;
}

/* ══════════════════════════════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════════════════════════════ */
.section-head {
    margin-bottom: 1.4rem;
}
.section-eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--primary-deep);
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 4px;
}
.section-eyebrow::before {
    content: "";
    display: inline-block;
    width: 20px; height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--accent-warm));
    border-radius: 2px;
}
.section-head h2 {
    font-family: 'Manrope', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    margin: 0 !important;
}
.section-head p {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 4px 0 0 !important;
    line-height: 1.6;
}

/* ══════════════════════════════════════════════════════════════
   GLASS CARD
══════════════════════════════════════════════════════════════ */
.glass-card {
    background: rgba(255,255,255,.80);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    padding: 1.6rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.2rem;
    transition: box-shadow .3s ease, transform .25s ease;
    animation: fadeUp .4s ease both;
}
.glass-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════════════════════════════════════════
   FEATURE CARDS (Dashboard)
══════════════════════════════════════════════════════════════ */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.feat-card {
    background: white;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    padding: 1.3rem 1.1rem;
    box-shadow: var(--shadow-xs);
    transition: all .28s cubic-bezier(.34,1.56,.64,1);
    position: relative; overflow: hidden;
    animation: fadeUp .4s ease both;
}
.feat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    opacity: 0;
    transition: opacity .25s ease;
}
.feat-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: var(--shadow-md);
    border-color: rgba(200,162,255,.40);
}
.feat-card:hover::before { opacity: 1; }
.feat-icon-wrap {
    width: 40px; height: 40px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 10px;
}
.feat-icon-lav  { background: rgba(200,162,255,.15); }
.feat-icon-sky  { background: rgba(186,230,253,.20); }
.feat-icon-peach{ background: rgba(255,214,204,.20); }
.feat-icon-mint { background: rgba(187,247,208,.18); }
.feat-icon-rose { background: rgba(254,205,211,.20); }
.feat-icon-amber{ background: rgba(253,230,138,.20); }
.feat-icon-violet{ background: rgba(221,214,254,.20); }
.feat-title {
    font-size: 0.84rem; font-weight: 700;
    color: var(--text); margin-bottom: 3px;
}
.feat-desc {
    font-size: 0.72rem;
    color: var(--text-muted);
    line-height: 1.55;
}
.feat-tag {
    display: inline-block;
    font-size: 0.62rem; font-weight: 600;
    padding: 2px 9px; border-radius: var(--radius-pill);
    margin-top: 7px; text-transform: uppercase; letter-spacing: .5px;
}
.tag-lav    { background: rgba(200,162,255,.15); color: var(--primary-deep); }
.tag-sky    { background: rgba(14,165,233,.10);  color: #0369A1; }
.tag-peach  { background: rgba(255,186,155,.18); color: #9A3412; }
.tag-mint   { background: rgba(16,185,129,.10);  color: #065F46; }
.tag-rose   { background: rgba(244,63,94,.10);   color: #9F1239; }
.tag-amber  { background: rgba(245,158,11,.10);  color: #78350F; }
.tag-violet { background: rgba(139,92,246,.10);  color: #4C1D95; }

/* ══════════════════════════════════════════════════════════════
   STAT CARDS
══════════════════════════════════════════════════════════════ */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: .85rem; margin-bottom: 1.5rem;
}
.stat-card {
    background: white;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    padding: 1.2rem 1rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-xs);
    transition: all .25s ease;
    animation: fadeUp .4s ease both;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-sm); }
.stat-num {
    font-family: 'Manrope', sans-serif;
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--primary-deep), var(--accent-warm));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}
.stat-lbl {
    font-size: 0.68rem; color: var(--text-light);
    text-transform: uppercase; letter-spacing: .6px;
    font-weight: 600; margin-top: 3px;
}
.stat-ico { font-size: 1.3rem; margin-bottom: 5px; }

/* ══════════════════════════════════════════════════════════════
   MESSAGE BOXES
══════════════════════════════════════════════════════════════ */
.msg {
    display: flex; align-items: flex-start; gap: 10px;
    padding: .9rem 1.2rem; border-radius: var(--radius);
    margin: .8rem 0; font-size: 0.84rem; font-weight: 500; line-height: 1.55;
    animation: fadeUp .3s ease both;
}
.msg-ico { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.msg-ok  { background: rgba(16,185,129,.07);  border: 1px solid rgba(16,185,129,.22); color: #065F46; }
.msg-inf { background: rgba(200,162,255,.10); border: 1px solid rgba(200,162,255,.30); color: var(--primary-deep); }
.msg-wrn { background: rgba(245,158,11,.07);  border: 1px solid rgba(245,158,11,.25);  color: #78350F; }

/* ══════════════════════════════════════════════════════════════
   IMAGE LABEL & FRAME
══════════════════════════════════════════════════════════════ */
.img-lbl {
    display: flex; align-items: center; gap: 7px;
    font-size: 0.72rem; font-weight: 700;
    color: var(--text-muted); text-transform: uppercase;
    letter-spacing: .8px; margin-bottom: 7px;
}
.img-lbl-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    flex-shrink: 0;
}

/* Images */
[data-testid="stImage"] img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow .25s ease, transform .25s ease;
}
[data-testid="stImage"] img:hover {
    box-shadow: var(--shadow-md) !important;
    transform: scale(1.005);
}
[data-testid="stImage"] p {
    font-size: 0.72rem !important;
    color: var(--text-light) !important;
    text-align: center; font-style: italic; margin-top: 5px !important;
}

/* ══════════════════════════════════════════════════════════════
   UPLOAD PROMPT
══════════════════════════════════════════════════════════════ */
.upload-prompt {
    text-align: center;
    padding: 3.5rem 2rem;
    background: rgba(255,255,255,.75);
    backdrop-filter: blur(12px);
    border-radius: var(--radius-lg);
    border: 2px dashed rgba(200,162,255,.35);
    margin: 1rem 0;
    animation: fadeUp .4s ease both;
}
.upload-prompt-ico { font-size: 3.5rem; display: block; margin-bottom: 1rem; }
.upload-prompt h3 {
    font-family: 'Manrope', sans-serif !important;
    font-size: 1.05rem !important; font-weight: 700 !important;
    color: var(--text) !important; margin-bottom: 6px !important;
}
.upload-prompt p { font-size: 0.8rem; color: var(--text-muted); line-height: 1.6; }

/* ══════════════════════════════════════════════════════════════
   BUTTONS & CONTROLS
══════════════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-deep)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-pill) !important;
    padding: 0.55rem 1.6rem !important;
    font-weight: 600 !important; font-size: 0.84rem !important;
    box-shadow: 0 4px 14px rgba(200,162,255,.38) !important;
    transition: all .25s ease !important;
    font-family: 'Poppins', sans-serif !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(200,162,255,.48) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Selectbox */
[data-baseweb="select"] > div {
    border-radius: var(--radius) !important;
    border-color: var(--border) !important;
    background: white !important;
    font-size: 0.85rem !important;
    transition: all .2s ease;
    box-shadow: var(--shadow-xs) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(200,162,255,.18) !important;
}

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: linear-gradient(90deg, var(--primary), var(--accent-warm)) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: white !important;
    border: 2.5px solid var(--primary) !important;
    box-shadow: 0 2px 8px rgba(200,162,255,.35) !important;
}

/* Radio */
[data-testid="stRadio"] label { font-size: 0.85rem !important; }

/* Metric */
[data-testid="stMetric"] {
    background: white;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-xs);
    text-align: center;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important; font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase; letter-spacing: .5px;
}
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important; font-weight: 800 !important;
    background: linear-gradient(135deg, var(--primary-deep), var(--accent-warm));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

h2, h3 { color: var(--text) !important; }

/* ══════════════════════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem 2rem !important; }
    .hero { grid-template-columns: 1fr; padding: 1.6rem 1.4rem; }
    .hero-orb { display: none; }
    .hero h1 { font-size: 1.6rem !important; }
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
    .feat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
    .feat-grid { grid-template-columns: 1fr; }
    .stat-grid { grid-template-columns: 1fr 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                         HERO HEADER                             ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<div class="hero">
  <div>
    <div class="hero-eyebrow">✦ Platform Pengolahan Citra</div>
    <h1>Crafting Beautiful<br><em>Image Processing</em></h1>
    <p class="hero-desc">
      Platform interaktif yang elegan untuk mempelajari dan menerapkan
      teknik pengolahan citra digital secara visual, intuitif, dan modern.
    </p>
    <div class="hero-stats">
      <div>
        <div class="hero-stat-num">7</div>
        <div class="hero-stat-label">Modul Fitur</div>
      </div>
      <div>
        <div class="hero-stat-num">20+</div>
        <div class="hero-stat-label">Operasi</div>
      </div>
      <div>
        <div class="hero-stat-num">5</div>
        <div class="hero-stat-label">Filter Spasial</div>
      </div>
      <div>
        <div class="hero-stat-num">4</div>
        <div class="hero-stat-label">Format Gambar</div>
      </div>
    </div>
  </div>
  <div class="hero-orb">🔬</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       SIDEBAR PROFESIONAL                       ║
# ╚══════════════════════════════════════════════════════════════════╝
st.sidebar.markdown("""
<div class="sb-logo">
  <div class="sb-logo-mark">✦</div>
  <span class="sb-logo-name">CITRA DIGITAL</span>
  <span class="sb-logo-sub">Image Processing Studio</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<span class="sb-section-label">✦ Navigasi</span>', unsafe_allow_html=True)

# ── Menu navigasi (TIDAK DIUBAH) ──────────────────────────────────
menu = st.sidebar.selectbox("Pilih Fitur:", [
    "🏠 Dashboard",
    "📁 Input & Tampilkan Gambar",
    "🎨 Grayscale & Citra Biner",
    "➕ Operasi Aritmatika",
    "🔣 Operasi Logika",
    "📊 Histogram",
    "🔍 Konvolusi & Filter",
    "🔷 Operasi Morfologi"
])

st.sidebar.markdown('<hr><span class="sb-section-label">✦ Upload Gambar</span>', unsafe_allow_html=True)

# ── Upload gambar (TIDAK DIUBAH) ───────────────────────────────────
image, img_array, filename = load_gambar(key="upload_gambar_utama")

if image is not None:
    st.sidebar.markdown(f"""
    <div class="msg msg-ok" style="margin-top:8px;padding:.6rem 1rem;font-size:.75rem;">
        <span class="msg-ico">✅</span>
        <div><b>{filename}</b><br>
        <span style="opacity:.75;font-size:.68rem;">{img_array.shape[1]}×{img_array.shape[0]} px
        &nbsp;·&nbsp; {img_array.shape[2] if len(img_array.shape)==3 else 1} ch</span></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown('<p class="sb-upload-note">JPG · PNG · BMP · JPEG</p>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                         HELPER FUNCTIONS                        ║
# ╚══════════════════════════════════════════════════════════════════╝
def no_image():
    st.markdown("""
    <div class="upload-prompt">
        <span class="upload-prompt-ico">🖼️</span>
        <h3>Belum Ada Gambar</h3>
        <p>Silakan upload gambar melalui panel <strong>Upload Gambar</strong>
        di sidebar kiri.<br>Format yang didukung: JPG, JPEG, PNG, BMP</p>
    </div>""", unsafe_allow_html=True)

def section_head(eyebrow, title, desc=""):
    st.markdown(f"""
    <div class="section-head">
        <div class="section-eyebrow">{eyebrow}</div>
        <h2>{title}</h2>
        {"<p>"+desc+"</p>" if desc else ""}
    </div>""", unsafe_allow_html=True)

def img_lbl(text):
    st.markdown(f'<div class="img-lbl"><span class="img-lbl-dot"></span>{text}</div>',
                unsafe_allow_html=True)

def ok(text):
    st.markdown(f'<div class="msg msg-ok"><span class="msg-ico">✅</span><div>{text}</div></div>',
                unsafe_allow_html=True)

def info(text):
    st.markdown(f'<div class="msg msg-inf"><span class="msg-ico">✦</span><div>{text}</div></div>',
                unsafe_allow_html=True)

def warn(text):
    st.markdown(f'<div class="msg msg-wrn"><span class="msg-ico">⚠️</span><div>{text}</div></div>',
                unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                     HALAMAN: DASHBOARD                          ║
# ╚══════════════════════════════════════════════════════════════════╝
if menu == "🏠 Dashboard":
    section_head("WHAT WE DO", "Thoughtful Design<br><em style='color:var(--primary-deep);font-style:italic'>for Modern Imaging</em>",
                 "Pilih modul dari sidebar dan mulai eksplorasi teknik pengolahan citra secara interaktif.")

    # Stat row
    st.markdown("""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-ico">🗂</div>
            <div class="stat-num">7</div><div class="stat-lbl">Kategori</div></div>
        <div class="stat-card"><div class="stat-ico">⚙️</div>
            <div class="stat-num">20+</div><div class="stat-lbl">Operasi</div></div>
        <div class="stat-card"><div class="stat-ico">🔍</div>
            <div class="stat-num">5</div><div class="stat-lbl">Filter</div></div>
        <div class="stat-card"><div class="stat-ico">🖼️</div>
            <div class="stat-num">4</div><div class="stat-lbl">Format</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards grid
    st.markdown("""
    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-lav">📁</div>
            <div class="feat-title">Input & Tampilkan</div>
            <div class="feat-desc">Upload dan lihat informasi detail gambar.</div>
            <span class="feat-tag tag-lav">Input</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-sky">🎨</div>
            <div class="feat-title">Grayscale & Biner</div>
            <div class="feat-desc">Konversi grayscale, biner manual & Otsu.</div>
            <span class="feat-tag tag-sky">Konversi</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-mint">➕</div>
            <div class="feat-title">Operasi Aritmatika</div>
            <div class="feat-desc">Penjumlahan, pengurangan, kali, bagi.</div>
            <span class="feat-tag tag-mint">Aritmatika</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-violet">🔣</div>
            <div class="feat-title">Operasi Logika</div>
            <div class="feat-desc">NOT, AND, OR, XOR pada piksel.</div>
            <span class="feat-tag tag-violet">Logika</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-amber">📊</div>
            <div class="feat-title">Histogram</div>
            <div class="feat-desc">Distribusi intensitas piksel gambar.</div>
            <span class="feat-tag tag-amber">Analisis</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-rose">🔍</div>
            <div class="feat-title">Konvolusi & Filter</div>
            <div class="feat-desc">Mean, Sharpening, Sobel, Prewitt.</div>
            <span class="feat-tag tag-rose">Filter</span>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap feat-icon-peach">🔷</div>
            <div class="feat-title">Morfologi</div>
            <div class="feat-desc">Erosi, Dilasi.</div>
            <span class="feat-tag tag-peach">Morfologi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How to use
    st.markdown("""
    <div class="glass-card" style="margin-top:.5rem;
         background:linear-gradient(135deg,rgba(200,162,255,.06),rgba(255,214,204,.05))">
        <div class="section-eyebrow" style="margin-bottom:.9rem">HOW TO USE</div>
        <div style="display:flex;flex-direction:column;gap:.75rem">
          <div style="display:flex;align-items:center;gap:14px;font-size:.85rem;color:var(--text)">
            <span style="min-width:28px;height:28px;background:linear-gradient(135deg,var(--primary),var(--primary-deep));
              color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;
              font-weight:700;font-size:.72rem;flex-shrink:0">1</span>
            <span><b>Upload gambar</b> di panel <em>Upload Gambar</em> pada sidebar kiri.</span>
          </div>
          <div style="display:flex;align-items:center;gap:14px;font-size:.85rem;color:var(--text)">
            <span style="min-width:28px;height:28px;background:linear-gradient(135deg,var(--secondary),var(--primary));
              color:var(--primary-deep);border-radius:50%;display:flex;align-items:center;justify-content:center;
              font-weight:700;font-size:.72rem;flex-shrink:0">2</span>
            <span><b>Pilih fitur</b> yang ingin digunakan dari dropdown navigasi.</span>
          </div>
          <div style="display:flex;align-items:center;gap:14px;font-size:.85rem;color:var(--text)">
            <span style="min-width:28px;height:28px;background:linear-gradient(135deg,var(--accent),var(--accent-warm));
              color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;
              font-weight:700;font-size:.72rem;flex-shrink:0">3</span>
            <span><b>Atur parameter</b> dan lihat hasil secara real-time.</span>
          </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Input & Tampilkan Gambar                  ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "📁 Input & Tampilkan Gambar":
    section_head("INPUT", "Input & Tampilkan Gambar", "Upload dan lihat informasi detail gambar Anda.")

    if image is not None:
        ok(f"Gambar berhasil diupload: <b>{filename}</b>")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # ── Fungsi asli TIDAK DIUBAH ──
        tampilkan_gambar(image, f"Gambar Asli — {filename}")
        get_info_gambar(img_array)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Grayscale & Citra Biner                   ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🎨 Grayscale & Citra Biner":
    section_head("KONVERSI", "Grayscale & Citra Biner", "Konversi gambar ke grayscale atau biner (manual / Otsu).")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Gambar Asli")
            # ── Logika asli TIDAK DIUBAH ──
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            pilihan = st.radio("Pilih Konversi:",
                               ["Grayscale", "Citra Biner Manual", "Citra Biner Otsu"])
            if pilihan == "Grayscale":
                hasil = konversi_grayscale(img_array)
                img_lbl("Hasil Grayscale")
                st.image(hasil, use_column_width=True, clamp=True)
            elif pilihan == "Citra Biner Manual":
                threshold = st.slider("Nilai Threshold (T):", 0, 255, 128)
                hasil = konversi_biner(img_array, threshold)
                img_lbl(f"Hasil Biner (T={threshold})")
                st.image(hasil, use_column_width=True, clamp=True)
            elif pilihan == "Citra Biner Otsu":
                hasil, t_val = konversi_biner_otsu(img_array)
                img_lbl(f"Hasil Biner Otsu (T={t_val:.0f})")
                st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Aritmatika                        ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "➕ Operasi Aritmatika":
    section_head("ARITMATIKA", "Operasi Aritmatika", "Terapkan operasi matematis pada nilai piksel gambar.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # ── Logika asli TIDAK DIUBAH ──
            operasi = st.selectbox("Pilih Operasi:",
                                   ["Penjumlahan", "Pengurangan", "Perkalian", "Pembagian"])
            if operasi in ["Penjumlahan", "Pengurangan"]:
                nilai = st.slider("Nilai:", 0, 255, 50)
            else:
                nilai = st.slider("Nilai:", 0.1, 3.0, 1.5)

            if operasi == "Penjumlahan":
                hasil = operasi_penjumlahan(img_array, int(nilai))
            elif operasi == "Pengurangan":
                hasil = operasi_pengurangan(img_array, int(nilai))
            elif operasi == "Perkalian":
                hasil = operasi_perkalian(img_array, nilai)
            else:
                hasil = operasi_pembagian(img_array, nilai)

            img_lbl(f"Hasil {operasi}")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Logika                            ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔣 Operasi Logika":
    section_head("LOGIKA", "Operasi Logika", "Operasi bitwise NOT, AND, OR, XOR pada citra.")

    if img_array is not None:
        # ── Logika asli TIDAK DIUBAH ──
        operasi = st.selectbox("Pilih Operasi Logika:", ["NOT", "AND", "OR", "XOR"])

        if operasi == "NOT":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                img_lbl("Gambar Asli")
                st.image(image, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                hasil = operasi_not(img_array)
                img_lbl("Hasil NOT")
                st.image(hasil, use_column_width=True, clamp=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            info("Upload gambar kedua untuk operasi <b>AND / OR / XOR</b>")
            image2, img_array2, filename2 = load_gambar(key="upload_gambar_kedua")
            if img_array2 is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    img_lbl("Gambar 1")
                    st.image(image, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    img_lbl("Gambar 2")
                    st.image(image2, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if operasi == "AND":
                        hasil = operasi_and(img_array, img_array2)
                    elif operasi == "OR":
                        hasil = operasi_or(img_array, img_array2)
                    else:
                        hasil = operasi_xor(img_array, img_array2)
                    img_lbl(f"Hasil {operasi}")
                    st.image(hasil, use_column_width=True, clamp=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Histogram                                 ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "📊 Histogram":
    section_head("ANALISIS", "Histogram Gambar", "Visualisasi distribusi intensitas piksel pada gambar.")

    if img_array is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Gambar Asli")
            # ── Fungsi asli TIDAK DIUBAH ──
            st.image(image, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Histogram")
            tampilkan_histogram(img_array)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Konvolusi & Filter                        ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔍 Konvolusi & Filter":
    section_head("FILTER", "Konvolusi & Filter Spasial", "Terapkan berbagai kernel filter pada gambar.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # ── Logika asli TIDAK DIUBAH ──
            filter_pilihan = st.selectbox("Pilih Filter:", [
                "Mean (Blur)",
                "Sharpening Standar",
                "Sharpening Kuat",
                "Edge Detection Sobel",
                "Edge Detection Prewitt"
            ])
            if filter_pilihan == "Mean (Blur)":
                kernel_size = st.slider("Ukuran Kernel:", 3, 11, 3, step=2)
                hasil = filter_mean(img_array, kernel_size)
            elif filter_pilihan == "Sharpening Standar":
                hasil = filter_sharpening(img_array, "standar")
            elif filter_pilihan == "Sharpening Kuat":
                hasil = filter_sharpening(img_array, "kuat")
            elif filter_pilihan == "Edge Detection Sobel":
                hasil = filter_sobel(img_array)
            else:
                hasil = filter_prewitt(img_array)

            img_lbl(f"Hasil {filter_pilihan}")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Morfologi                         ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔷 Operasi Morfologi":
    section_head("MORFOLOGI", "Operasi Morfologi", "Transformasi bentuk: Erosi, Dilasi, Opening, Closing.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            img_lbl("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # ── Logika asli TIDAK DIUBAH ──
            operasi_morf = st.selectbox("Pilih Operasi:", [
                "Erosi", "Dilasi", "Opening", "Closing"
            ])
            se_pilihan = st.selectbox("Pilih Elemen Penstruktur (SE):", [
                "silang", "kotak", "diagonal", "vertikal", "horizontal"
            ])
            if operasi_morf == "Erosi":
                hasil = erosi(img_array, se_pilihan)
            elif operasi_morf == "Dilasi":
                hasil = dilasi(img_array, se_pilihan)
            elif operasi_morf == "Opening":
                hasil = opening(img_array, se_pilihan)
            else:
                hasil = closing(img_array, se_pilihan)

            img_lbl(f"Hasil {operasi_morf} ({se_pilihan})")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        no_image()
