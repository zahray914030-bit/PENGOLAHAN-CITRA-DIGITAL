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
    page_icon="🖼️",
    layout="wide"
)

# ╔══════════════════════════════════════════════════════════════════╗
# ║                    CUSTOM CSS — UI MODERN                       ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
/* ── Import Font Modern ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Variabel Warna Global ──────────────────────────────────── */
:root {
    --primary:        #2563EB;
    --primary-light:  #3B82F6;
    --primary-dark:   #1D4ED8;
    --secondary:      #0EA5E9;
    --accent:         #14B8A6;
    --accent-light:   #2DD4BF;
    --bg:             #F0F4FF;
    --card-bg:        #FFFFFF;
    --sidebar-bg:     #0F172A;
    --text:           #1E293B;
    --text-muted:     #64748B;
    --text-light:     #94A3B8;
    --border:         #E2E8F0;
    --border-focus:   #2563EB;
    --success:        #10B981;
    --warning:        #F59E0B;
    --error:          #EF4444;
    --info:           #3B82F6;
    --shadow-sm:      0 1px 3px rgba(37,99,235,.08), 0 1px 2px rgba(0,0,0,.06);
    --shadow-md:      0 4px 16px rgba(37,99,235,.10), 0 2px 8px rgba(0,0,0,.06);
    --shadow-lg:      0 8px 32px rgba(37,99,235,.14), 0 4px 16px rgba(0,0,0,.08);
    --radius:         14px;
    --radius-lg:      20px;
    --radius-xl:      28px;
}

/* ── Reset & Base ───────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    color: var(--text);
}

/* ── Background Utama ───────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0FAFB 50%, #F0F4FF 100%);
    background-attachment: fixed;
}

/* ── Sembunyikan elemen default Streamlit yang tidak perlu ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar Profesional ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 60%, #0F172A 100%) !important;
    border-right: 1px solid rgba(255,255,255,.06);
    box-shadow: 4px 0 24px rgba(0,0,0,.25);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 0 1rem 1rem !important;
}

/* Teks sidebar */
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
}

/* Selectbox sidebar */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: var(--radius) !important;
    color: #E2E8F0 !important;
    transition: all .2s ease;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    border-color: var(--primary-light) !important;
    background: rgba(59,130,246,.12) !important;
}

/* File uploader sidebar */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,.04) !important;
    border: 1.5px dashed rgba(59,130,246,.4) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem !important;
    transition: all .2s ease;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: var(--primary-light) !important;
    background: rgba(59,130,246,.08) !important;
}

/* Divider sidebar */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.08) !important;
    margin: 0.6rem 0 !important;
}

/* ── Konten Utama ───────────────────────────────────────────── */
.main .block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1200px;
}

/* ── Header Aplikasi (gradient judul) ───────────────────────── */
.app-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 40%, #0EA5E9 80%, #14B8A6 100%);
    border-radius: var(--radius-xl);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.app-header::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,.06);
    border-radius: 50%;
    pointer-events: none;
}
.app-header::after {
    content: "";
    position: absolute;
    bottom: -60%;
    left: 5%;
    width: 200px;
    height: 200px;
    background: rgba(255,255,255,.04);
    border-radius: 50%;
    pointer-events: none;
}
.app-header h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    margin: 0 0 0.3rem !important;
    letter-spacing: -0.5px;
}
.app-header p {
    font-size: 0.95rem;
    opacity: .85;
    margin: 0;
    font-weight: 400;
}
.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.25);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: .5px;
    text-transform: uppercase;
}

/* ── Card / Container Universal ────────────────────────────── */
.card {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
    margin-bottom: 1.2rem;
    transition: box-shadow .25s ease, transform .2s ease;
}
.card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-1px);
}

/* ── Page Section Header ────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, rgba(37,99,235,.07), rgba(14,165,233,.04));
    border-radius: var(--radius);
    border-left: 4px solid var(--primary);
    margin-bottom: 1.2rem;
}
.section-header-icon {
    font-size: 1.6rem;
    line-height: 1;
}
.section-header-text h2 {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    margin: 0 !important;
}
.section-header-text p {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 2px 0 0 !important;
}

/* ── Stat Cards (Dashboard) ─────────────────────────────────── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.stat-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: all .2s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
}
.stat-card.blue::before   { background: var(--primary); }
.stat-card.sky::before    { background: var(--secondary); }
.stat-card.teal::before   { background: var(--accent); }
.stat-card.indigo::before { background: #6366F1; }
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: .4px;
}
.stat-icon { font-size: 1.5rem; margin-bottom: 6px; }

/* ── Feature Cards (Dashboard) ─────────────────────────────── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.feature-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1.2rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: all .25s ease;
    cursor: default;
}
.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-light);
}
.feature-card-icon {
    font-size: 1.8rem;
    margin-bottom: 8px;
    display: block;
}
.feature-card-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}
.feature-card-desc {
    font-size: 0.75rem;
    color: var(--text-muted);
    line-height: 1.5;
}
.feature-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: .4px;
}
.badge-blue   { background: rgba(37,99,235,.1);   color: var(--primary); }
.badge-sky    { background: rgba(14,165,233,.1);  color: var(--secondary); }
.badge-teal   { background: rgba(20,184,166,.1);  color: var(--accent); }
.badge-indigo { background: rgba(99,102,241,.1);  color: #6366F1; }
.badge-amber  { background: rgba(245,158,11,.1);  color: #D97706; }
.badge-rose   { background: rgba(244,63,94,.1);   color: #E11D48; }
.badge-violet { background: rgba(139,92,246,.1);  color: #7C3AED; }

/* ── Status Messages ────────────────────────────────────────── */
.msg-box {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 1rem 1.25rem;
    border-radius: var(--radius);
    margin: 0.75rem 0;
    font-size: 0.88rem;
    font-weight: 500;
    line-height: 1.5;
}
.msg-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 1px; }
.msg-success {
    background: rgba(16,185,129,.08);
    border: 1px solid rgba(16,185,129,.25);
    color: #065F46;
}
.msg-warning {
    background: rgba(245,158,11,.08);
    border: 1px solid rgba(245,158,11,.25);
    color: #78350F;
}
.msg-error {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.25);
    color: #7F1D1D;
}
.msg-info {
    background: rgba(59,130,246,.08);
    border: 1px solid rgba(59,130,246,.20);
    color: #1E3A8A;
}

/* ── Label Gambar ───────────────────────────────────────────── */
.img-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.img-label::before {
    content: "";
    display: inline-block;
    width: 3px;
    height: 14px;
    background: var(--primary);
    border-radius: 2px;
}

/* Wrapper gambar dengan border halus */
[data-testid="stImage"] img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow .2s ease;
}
[data-testid="stImage"] img:hover {
    box-shadow: var(--shadow-md) !important;
}
[data-testid="stImage"] p {
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    text-align: center;
    font-style: italic;
    margin-top: 4px !important;
}

/* ── Tombol ─────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: .2px;
    transition: all .2s ease !important;
    box-shadow: 0 2px 8px rgba(37,99,235,.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(37,99,235,.35) !important;
    background: linear-gradient(135deg, var(--primary-light), var(--primary)) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(37,99,235,.3) !important;
}

/* ── Input / Selectbox / Slider ─────────────────────────────── */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    border-radius: var(--radius) !important;
    border-color: var(--border) !important;
    background: var(--card-bg) !important;
    font-size: 0.88rem !important;
    transition: border-color .2s ease, box-shadow .2s ease;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"] > div:focus-within {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
}

/* Slider track */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--primary) !important;
    border-color: white !important;
    box-shadow: 0 2px 6px rgba(37,99,235,.35) !important;
}

/* Radio */
[data-testid="stRadio"] label {
    font-size: 0.88rem !important;
}
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-weight: 500;
}

/* ── Metric Cards ───────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1rem !important;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    text-align: center;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: .4px;
}
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: var(--primary) !important;
}

/* ── Subheader Styling ──────────────────────────────────────── */
h2, .stSubheader {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}
h3 { font-size: 0.92rem !important; font-weight: 600 !important; }

/* ── Divider ────────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Sidebar Logo Area ──────────────────────────────────────── */
.sidebar-logo {
    text-align: center;
    padding: 1.6rem 1rem 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,.08);
    margin-bottom: 1rem;
}
.sidebar-logo-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 12px rgba(59,130,246,.6));
}
.sidebar-logo-title {
    font-size: 0.92rem;
    font-weight: 800;
    color: #F1F5F9 !important;
    letter-spacing: .5px;
    display: block;
}
.sidebar-logo-sub {
    font-size: 0.7rem;
    color: #64748B !important;
    display: block;
    margin-top: 2px;
}
.sidebar-section-label {
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569 !important;
    padding: 0.5rem 0 0.3rem;
    display: block;
}
.sidebar-upload-hint {
    font-size: 0.72rem;
    color: #475569 !important;
    text-align: center;
    padding: 4px 0;
}

/* ── Upload Hint di Konten Utama ────────────────────────────── */
.upload-prompt {
    text-align: center;
    padding: 3rem 1.5rem;
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    border: 2px dashed var(--border);
    margin: 1rem 0;
}
.upload-prompt-icon { font-size: 3rem; display: block; margin-bottom: 1rem; }
.upload-prompt h3 {
    font-size: 1rem !important;
    color: var(--text) !important;
    margin-bottom: 6px !important;
}
.upload-prompt p {
    font-size: 0.82rem;
    color: var(--text-muted);
}

/* ── Responsif ──────────────────────────────────────────────── */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem !important; }
    .app-header { padding: 1.4rem 1.2rem; }
    .app-header h1 { font-size: 1.4rem !important; }
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
    .feature-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
    .stat-grid { grid-template-columns: 1fr 1fr; }
    .feature-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                  HEADER APLIKASI (GRADIENT)                     ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<div class="app-header">
    <div class="header-badge">✦ Platform Digital Imaging</div>
    <h1>🖼️ Pengolahan Citra Digital</h1>
    <p>Platform interaktif untuk mempelajari dan menerapkan teknik pengolahan citra digital secara visual dan informatif.</p>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       SIDEBAR PROFESIONAL                       ║
# ╚══════════════════════════════════════════════════════════════════╝
# -- Logo & brand sidebar
st.sidebar.markdown("""
<div class="sidebar-logo">
    <span class="sidebar-logo-icon">🔬</span>
    <span class="sidebar-logo-title">CITRA DIGITAL</span>
    <span class="sidebar-logo-sub">Image Processing Platform</span>
</div>
""", unsafe_allow_html=True)

# -- Label navigasi
st.sidebar.markdown('<span class="sidebar-section-label">🗂 Navigasi Fitur</span>', unsafe_allow_html=True)

# ── Menu utama (TIDAK DIUBAH) ──────────────────────────────────────
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

# -- Label upload
st.sidebar.markdown('<hr><span class="sidebar-section-label">📤 Upload Gambar</span>', unsafe_allow_html=True)

# ── Upload Gambar (selalu tampil — TIDAK DIUBAH) ────────────────────
image, img_array, filename = load_gambar()

# -- Info singkat di sidebar jika gambar sudah diupload
if image is not None:
    st.sidebar.markdown(f"""
    <div class="msg-box msg-success" style="margin-top:8px;padding:.6rem 1rem;font-size:.78rem;">
        <span class="msg-icon">✅</span>
        <div><b>{filename}</b><br>
        <span style="font-size:.72rem;opacity:.8;">{img_array.shape[1]}×{img_array.shape[0]} px &nbsp;|&nbsp; {img_array.shape[2] if len(img_array.shape)==3 else 1}ch</span></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown('<p class="sidebar-upload-hint">Format: JPG · PNG · BMP</p>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                    HELPER — STATUS MESSAGES                     ║
# ╚══════════════════════════════════════════════════════════════════╝
def info_upload():
    """Tampilkan pesan prompt upload gambar yang lebih menarik."""
    st.markdown("""
    <div class="upload-prompt">
        <span class="upload-prompt-icon">📂</span>
        <h3>Belum Ada Gambar</h3>
        <p>Silakan upload gambar melalui panel <strong>Upload Gambar</strong> di sidebar kiri<br>
        (Format yang didukung: JPG, JPEG, PNG, BMP)</p>
    </div>
    """, unsafe_allow_html=True)

def section_header(icon, title, desc=""):
    """Render header section yang konsisten di setiap halaman."""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-icon">{icon}</div>
        <div class="section-header-text">
            <h2>{title}</h2>
            {"<p>"+desc+"</p>" if desc else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

def img_label(text):
    """Label di atas gambar yang konsisten."""
    st.markdown(f'<div class="img-label">{text}</div>', unsafe_allow_html=True)

def success_msg(text):
    st.markdown(f'<div class="msg-box msg-success"><span class="msg-icon">✅</span><div>{text}</div></div>', unsafe_allow_html=True)

def info_msg(text):
    st.markdown(f'<div class="msg-box msg-info"><span class="msg-icon">ℹ️</span><div>{text}</div></div>', unsafe_allow_html=True)

def warning_msg(text):
    st.markdown(f'<div class="msg-box msg-warning"><span class="msg-icon">⚠️</span><div>{text}</div></div>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                    HALAMAN: DASHBOARD                           ║
# ╚══════════════════════════════════════════════════════════════════╝
if menu == "🏠 Dashboard":
    section_header("🏠", "Selamat Datang!", "Pilih fitur dari sidebar untuk memulai pengolahan citra.")

    # -- Statistik fitur
    st.markdown("""
    <div class="stat-grid">
        <div class="stat-card blue">
            <div class="stat-icon">🗂</div>
            <div class="stat-number">7</div>
            <div class="stat-label">Kategori Fitur</div>
        </div>
        <div class="stat-card sky">
            <div class="stat-icon">⚙️</div>
            <div class="stat-number">20+</div>
            <div class="stat-label">Operasi</div>
        </div>
        <div class="stat-card teal">
            <div class="stat-icon">🖼️</div>
            <div class="stat-number">4</div>
            <div class="stat-label">Format Gambar</div>
        </div>
        <div class="stat-card indigo">
            <div class="stat-icon">📐</div>
            <div class="stat-number">5</div>
            <div class="stat-label">Filter Spasial</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -- Daftar fitur
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:.78rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:.8rem">📋 Fitur yang Tersedia</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-card-icon">📁</span>
            <div class="feature-card-title">Input & Tampilkan</div>
            <div class="feature-card-desc">Upload dan lihat informasi detail gambar.</div>
            <span class="feature-badge badge-blue">Input</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">🎨</span>
            <div class="feature-card-title">Grayscale & Biner</div>
            <div class="feature-card-desc">Konversi ke grayscale, biner manual & Otsu.</div>
            <span class="feature-badge badge-sky">Konversi</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">➕</span>
            <div class="feature-card-title">Operasi Aritmatika</div>
            <div class="feature-card-desc">Penjumlahan, pengurangan, perkalian, pembagian.</div>
            <span class="feature-badge badge-teal">Aritmatika</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">🔣</span>
            <div class="feature-card-title">Operasi Logika</div>
            <div class="feature-card-desc">NOT, AND, OR, XOR pada piksel gambar.</div>
            <span class="feature-badge badge-indigo">Logika</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">📊</span>
            <div class="feature-card-title">Histogram</div>
            <div class="feature-card-desc">Visualisasi distribusi intensitas piksel.</div>
            <span class="feature-badge badge-amber">Analisis</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">🔍</span>
            <div class="feature-card-title">Konvolusi & Filter</div>
            <div class="feature-card-desc">Mean, Sharpening, Sobel, Prewitt.</div>
            <span class="feature-badge badge-rose">Filter</span>
        </div>
        <div class="feature-card">
            <span class="feature-card-icon">🔷</span>
            <div class="feature-card-title">Operasi Morfologi</div>
            <div class="feature-card-desc">Erosi, Dilasi, Opening, Closing.</div>
            <span class="feature-badge badge-violet">Morfologi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -- Cara penggunaan
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="background:linear-gradient(135deg,rgba(37,99,235,.04),rgba(14,165,233,.03))">
        <p style="font-size:.78rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin:0 0 .8rem">🚀 Cara Penggunaan</p>
        <div style="display:flex;flex-direction:column;gap:.6rem">
            <div style="display:flex;align-items:center;gap:12px;font-size:.85rem">
                <span style="min-width:26px;height:26px;background:var(--primary);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.75rem">1</span>
                <span><b>Upload gambar</b> di panel <em>Upload Gambar</em> pada sidebar kiri.</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;font-size:.85rem">
                <span style="min-width:26px;height:26px;background:var(--secondary);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.75rem">2</span>
                <span><b>Pilih fitur</b> yang ingin digunakan dari dropdown menu navigasi.</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;font-size:.85rem">
                <span style="min-width:26px;height:26px;background:var(--accent);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.75rem">3</span>
                <span><b>Atur parameter</b> sesuai kebutuhan dan lihat hasilnya secara langsung.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Input & Tampilkan Gambar                  ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "📁 Input & Tampilkan Gambar":
    section_header("📁", "Input & Tampilkan Gambar", "Upload dan lihat informasi detail gambar Anda.")

    if image is not None:
        success_msg(f"Gambar berhasil diupload: <b>{filename}</b>")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # ── Fungsi asli — TIDAK DIUBAH ──
        tampilkan_gambar(image, f"Gambar Asli — {filename}")
        get_info_gambar(img_array)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Grayscale & Citra Biner                   ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🎨 Grayscale & Citra Biner":
    section_header("🎨", "Grayscale & Citra Biner", "Konversi gambar ke grayscale atau biner (manual/Otsu).")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Gambar Asli")
            # ── Fungsi asli — TIDAK DIUBAH ──
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # ── Logika asli — TIDAK DIUBAH ──
            pilihan = st.radio("Pilih Konversi:",
                               ["Grayscale", "Citra Biner Manual", "Citra Biner Otsu"])

            if pilihan == "Grayscale":
                hasil = konversi_grayscale(img_array)
                img_label("Hasil Grayscale")
                st.image(hasil, use_column_width=True, clamp=True)

            elif pilihan == "Citra Biner Manual":
                threshold = st.slider("Nilai Threshold (T):", 0, 255, 128)
                hasil = konversi_biner(img_array, threshold)
                img_label(f"Hasil Biner (T={threshold})")
                st.image(hasil, use_column_width=True, clamp=True)

            elif pilihan == "Citra Biner Otsu":
                hasil, t_val = konversi_biner_otsu(img_array)
                img_label(f"Hasil Biner Otsu (T={t_val:.0f})")
                st.image(hasil, use_column_width=True, clamp=True)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Aritmatika                        ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "➕ Operasi Aritmatika":
    section_header("➕", "Operasi Aritmatika", "Terapkan operasi matematika pada nilai piksel gambar.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # ── Logika asli — TIDAK DIUBAH ──
            operasi = st.selectbox("Pilih Operasi:",
                                   ["Penjumlahan", "Pengurangan",
                                    "Perkalian", "Pembagian"])

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

            img_label(f"Hasil {operasi}")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Logika                            ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔣 Operasi Logika":
    section_header("🔣", "Operasi Logika", "Operasi bitwise NOT, AND, OR, XOR pada citra.")

    if img_array is not None:
        # ── Logika asli — TIDAK DIUBAH ──
        operasi = st.selectbox("Pilih Operasi Logika:",
                               ["NOT", "AND", "OR", "XOR"])

        if operasi == "NOT":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                img_label("Gambar Asli")
                st.image(image, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                hasil = operasi_not(img_array)
                img_label("Hasil NOT")
                st.image(hasil, use_column_width=True, clamp=True)
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            info_msg("Upload gambar kedua untuk operasi <b>AND / OR / XOR</b>")
            image2, img_array2, filename2 = load_gambar()

            if img_array2 is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    img_label("Gambar 1")
                    st.image(image, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    img_label("Gambar 2")
                    st.image(image2, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    if operasi == "AND":
                        hasil = operasi_and(img_array, img_array2)
                    elif operasi == "OR":
                        hasil = operasi_or(img_array, img_array2)
                    else:
                        hasil = operasi_xor(img_array, img_array2)
                    img_label(f"Hasil {operasi}")
                    st.image(hasil, use_column_width=True, clamp=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Histogram                                 ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "📊 Histogram":
    section_header("📊", "Histogram Gambar", "Visualisasi distribusi intensitas piksel pada gambar.")

    if img_array is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Gambar Asli")
            # ── Fungsi asli — TIDAK DIUBAH ──
            st.image(image, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Histogram Gambar")
            tampilkan_histogram(img_array)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Konvolusi & Filter                        ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔍 Konvolusi & Filter":
    section_header("🔍", "Konvolusi & Filter Spasial", "Terapkan berbagai kernel filter pada gambar.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # ── Logika asli — TIDAK DIUBAH ──
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

            img_label(f"Hasil {filter_pilihan}")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()


# ╔══════════════════════════════════════════════════════════════════╗
# ║              HALAMAN: Operasi Morfologi                         ║
# ╚══════════════════════════════════════════════════════════════════╝
elif menu == "🔷 Operasi Morfologi":
    section_header("🔷", "Operasi Morfologi", "Transformasi bentuk: Erosi, Dilasi, Opening, Closing.")

    if img_array is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_label("Gambar Asli")
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # ── Logika asli — TIDAK DIUBAH ──
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

            img_label(f"Hasil {operasi_morf} ({se_pilihan})")
            st.image(hasil, use_column_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        info_upload()
