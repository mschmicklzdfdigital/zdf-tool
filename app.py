import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BERLIN MINIMALIST DARK THEME (HIGH-END EDITORIAL 2026)
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background-color: #05070c !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #05070c; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #ff5a00; }

p, li, span, label, .stMarkdown {
    color: #94a3b8 !important;
    font-size: 15px !important;
}

.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 0 15px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 30px;
}

.shimmer-title {
    font-size: 28px !important;
    font-weight: 800 !important;
    letter-spacing: -1.2px;
    background: linear-gradient(120deg, #ffffff 30%, #ff7a22 50%, #ffffff 70%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.live-dot-de {
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: #ff5a00;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}

.editorial-info-box {
    background: #0d111c;
    border-left: 3px solid #ff5a00;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 35px;
    font-size: 14.5px;
    color: #cbd5e1 !important;
    line-height: 1.5;
}

[data-testid="stFileUploader"] {
    background: #0d111c !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 18px !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #ff5a00 !important;
}
[data-testid="stFileUploader"] label p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.clean-kpi-container {
    padding: 25px 0;
    margin: 25px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.kpi-shimmer-number {
    font-size: 38px !important;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #ff5a00 0%, #ff9e66 50%, #ff5a00 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 5s linear infinite;
}

.section-headline {
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 40px 0 15px 0;
}

.news-card {
    background: #0d111c;
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}
.news-card:hover {
    border-color: rgba(255, 90, 0, 0.3);
    transform: translateY(-1px);
}
.news-headline {
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #ffffff !important;
    margin-bottom: 6px;
}
.news-url-anchor {
    font-size: 13px !important;
    color: #64748b !important;
    text-decoration: none;
}
.news-card:hover .news-url-anchor {
    color: #ff9e66 !important;
}

.guide-container {
    background: #0d111c;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    padding: 25px;
    margin-top: 60px;
}
.guide-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
}
.guide-step {
    margin-bottom: 10px;
    line-height: 1.5;
    color: #94a3b8 !important;
}
.guide-step strong {
    color: #cbd5e1 !important;
}

.feedback-box {
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 60px;
}
.feedback-title {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# SHIMMER BRAND HEADER WITH AUTOMATIC JS-CLOCK
# =========================================================
header_html = """
<div class="brand-header">
    <div class="shimmer-title">
        ZDFheute 🧡 ZDF Digital <span style="color:rgba(255,255,255,0.15); font-weight:300; margin:0 8px;">|</span> WhatsApp Artikel-Checker
    </div>
    <div style="text-align: right; font-size: 11px; color: #475569; font-weight: 600; letter-spacing: 0.5px;">
        <span class="live-dot-de"></span><span style="color: #64748b;">LIVE-DATEN AKTIV</span><br>
        <span id="live-ticker-2026" style="color: #475569; font-weight: 500; display:block; margin-top:2px; font-variant-numeric: tabular-nums;">--.--.---- - --:--:--</span>
    </div>
</div>

<script>
function updateClock() {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    const timeString = `${day}.${month}.${year} - ${hours}:${minutes}:${seconds}`;
    const el = document.getElementById('live-ticker-2026');
    if (el) { el.innerHTML = timeString; }
}
setInterval(updateClock, 1000);
updateClock();
</script>
"""
st.markdown(header_html, unsafe_allow_html=True)

# =========================================================
# SYSTEM-LOGIK MIT WEGWEISER NACH UNTEN
# =========================================================
st.markdown("""
<div class="editorial-info-box">
    Dieses Tool gleicht ab, welche Artikel, die in der ZDFheute App und auf Web veröffentlicht wurden, bereits auf dem WhatsApp-Kanal der ZDFheute erschienen sind. Am Ende zeigt es dir nur die Artikel an, die noch nicht publiziert wurden – gefiltert nach den Kategorien, die die Userinnen und User am meisten interessieren.<br><br>
    💡 <strong>Du weißt nicht, wie du die benötigte Datei aus Piano ziehst?</strong> Eine Schritt-für-Schritt-Anleitung findest du ganz unten auf dieser Seite.
</div>
""", unsafe_allow_html=True)

# =========================================================
# KONTROLL-PANEL MATRIZ
# =========================================================
col_file, col_d1, col_d2 = st.columns([2, 1, 1])

with col_file:
    file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])

with col_d1:
    start_date = st.date_input("Startdatum", value=date.today(), format="DD.MM.YYYY")

with col_d2:
    end_date = st.date_input("Enddatum", value=date.today(), format="DD.MM.YYYY")

if start_date > end_date:
    st.error("Fehler: Das Startdatum darf nicht nach dem Enddatum liegen.")
    st.stop()

start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# =========================================================
# EXCLUSION ENGINE & VALIDATOR
# =========================================================
def should_filter_out(url):
    u = url.lower().strip()
    if "zdf.de/dokumentation" in u or "zdf.de/dokus" in u: return True
    if "lottozahlen.zdf.de" in u: return True
    if "zdf.de/video" in u or "zdfheute.de/video" in u or "/video/" in u: return True
    if "zdfheute.de/briefing" in u or "zdf.de/briefing" in u or "/briefing" in u: return True
    if "zdfheute.de/thema" in u or "zdf.de/thema" in u or "/thema/" in u: return True
    if "zdfheute.de/in-eigener-sache" in u or "zdf.de/in-eigener-sache" in u: return True
    if "phoenix.de" in u: return True
    
    clean_url = u.replace("https://", "").replace("http://", "").replace("www.", "")
    parts =
