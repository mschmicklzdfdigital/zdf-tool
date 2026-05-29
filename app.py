import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import time

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
    padding: 20px 24px;
    border-radius: 0 8px 8px 0;
    margin: 40px 0;
    font-size: 14.5px;
    color: #cbd5e1 !important;
    line-height: 1.6;
}

.info-bullet-list {
    margin-top: 15px;
    padding-left: 5px;
}

.info-bullet-item {
    margin-bottom: 12px;
    color: #94a3b8 !important;
}

.info-bullet-item strong {
    color: #ffffff !important;
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

div.stDownloadButton > button {
    background-color: transparent !important;
    color: #ff5a00 !important;
    border: 1px solid rgba(255, 90, 0, 0.3) !important;
    padding: 8px 16px !important;
    font-size: 13.5px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
    margin-top: 5px !important;
    width: 100% !important;
    text-align: left !important;
}
div.stDownloadButton > button:hover {
    background-color: rgba(255, 90, 0, 0.08) !important;
    border-color: #ff5a00 !important;
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

.feedback-box {
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 80px;
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
# KONTROLL-PANEL & ANLEITUNG
# =========================================================
col_file, col_d1, col_d2 = st.columns([2, 1, 1])
with col_file: file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col_d1: start_date = st.date_input("Startdatum", value=(datetime.now() - timedelta(days=datetime.now().weekday())), format="DD.MM.YYYY")
with col_d2: end_date = st.date_input("Enddatum", value=date.today(), format="DD.MM.YYYY")

guide_text = """ANLEITUNG: EXCEL-EXPORT AUS PIANO ANALYTICS (WINDOWS)
1. Oeffne dein Piano-Analytics-Dashboard.
2. Navigiere zum Board "Zugriffe via WhatsApp-AT-Parameter".
3. Stelle sicher, dass der Zeitraum oben im Dashboard dem gewünschten Bereich entspricht.
4. Scrolle zur Haupttabelle, die alle gesendeten Artikel-Links listet.
5. Klicke in der Tabelle oben rechts auf das Drei-Punkte-Menü (...).
6. Waehle "Die ersten 10.000 Zeilen dieser Tabelle herunterladen".
7. Importiere die Datei in Excel als UTF-8 CSV und speichere sie als .xlsx."""

st.download_button("💡 Du weißt nicht, wie du die Datei bekommst? Anleitung hier laden.", guide_text, file_name="Anleitung_Piano_Export.txt")

# =========================================================
# EDITORIALER KATEGORIEN-KASTEN
# =========================================================
st.markdown("""
<div class="editorial-info-box">
    Dieses Tool gleicht ab, welche Web/App-Artikel von ZDFheute bereits auf dem WhatsApp-Kanal der ZDFheute erschienen sind. Am Ende zeigt es dir nur die Artikel an, die noch nicht publiziert wurden – gefiltert nach den Kategorien, die die User*innen am meisten interessieren:
    <div class="info-bullet-list">
        <div class="info-bullet-item"><strong>• Macht und Folgen:</strong> Politik & Analysen. Tiefe Einblicke.</div>
        <div class="info-bullet-item"><strong>• Gut zu wissen:</strong> Service, Ratgeber & Wetter.</div>
        <div class="info-bullet-item"><strong>• Zwischen Tat und Aufklärung:</strong> True Crime & Kriminalität.</div>
        <div class="info-bullet-item"><strong>• Trends, Pop & Kurioses:</strong> Trends & Unterhaltung.</div>
        <div class="info-bullet-item"><strong>• Sonstige Artikel:</strong> Alle weiteren Inhalte.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LOGIK: VERARBEITUNG & SUCH-ENGINE
# =========================================================
def get_slug(url): return url.strip('/').split('/')[-1].split('?')[0].lower()

def should_filter_out(url):
    u = url.lower()
    return any(x in u for x in ["presseportal", "newsticker", "video", "briefing", "thema", "in-eigener-sache", "phoenix"])

def categorize(title, url):
    t, u = title.lower(), url.lower()
    if any(x in t for x in ["mord", "tat", "gericht", "polizei", "kriminal", "prozess", "ermittlung"]): return "Zwischen Tat und Aufklärung"
    if any(x in t for x in ["wetter", "rezept", "geld", "ratgeber", "ernährung", "tipps"]): return "Gut zu wissen"
    if any(x in u for x in ["politik", "bundestag", "scholz", "habeck"]): return "Macht und Folgen"
    if any(x in t for x in ["promi", "tiktok", "viral", "film", "musik", "show"]): return "Trends, Pop & Kurioses"
    return "Sonstige Artikel"

def get_articles_from_search(max_pages=15):
    all_articles = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, max_pages + 1):
        try:
            r = requests.get(f"https://www.zdfheute.de/suche?q=*&type=all&page={page}", headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            for item in soup.select('div.teaser-full__body, div.teaser-standard__body'):
                link_tag = item.find('a', href=True)
                title_tag = item.find(['h2', 'h3'], class_=['teaser-full__headline', 'teaser-standard__headline'])
                if link_tag and title_tag:
                    all_articles.append({"title": title_tag.get_text(strip=True), "url": "https://www.zdfheute.de" + link_tag['href']})
        except: continue
        time.sleep(0.3)
    return all_articles

if file:
    df = pd.read_excel(file, engine="openpyxl")
    excel_slugs = {get_slug(str(url)) for url in df.iloc[:,1].dropna()} if df.shape[1] > 1 else set()
    
    online_articles = get_articles_from_search()
    target_categories = ["Macht und Folgen", "Gut zu wissen", "Zwischen Tat und Aufklärung", "Trends, Pop & Kurioses", "Sonstige Artikel"]
    grouped = {cat: [] for cat in target_categories}
    
    for a in online_articles:
        if get_slug(a["url"]) in excel_slugs or should_filter_out(a["url"]): continue
        cat = categorize(a["title"], a["url"])
        if cat in grouped: grouped[cat].append(a)

    total_missing = sum(len(v) for v in grouped.values())
    st.markdown(f'<div class="clean-kpi-container"><div class="kpi-shimmer-number">Fehlende Artikel: {total_missing}</div></div>', unsafe_allow_html=True)
    
    for cat in target_categories:
        if grouped[cat]:
            st.markdown(f'<div class="section-headline">{cat}</div>', unsafe_allow_html=True)
            for item in grouped[cat]:
                st.markdown(f'<div class="news-card"><div class="news-headline">{item["title"]}</div><a href="{item["url"]}" class="news-url-anchor">{item["url"]}</a></div>', unsafe_allow_html=True)

# =========================================================
# FEEDBACK FOOTER
# =========================================================
st.markdown("""
<div class="feedback-box">
    <div class="feedback-title">Du hast Feedback? <span style="color:#ff5a00;">🧡</span></div>
    <div style="margin-top:6px; font-size:13px; color: #64748b;">Schreibe direkt an <strong>Matthias Schmickl</strong>.</div>
</div>
""", unsafe_allow_html=True)
