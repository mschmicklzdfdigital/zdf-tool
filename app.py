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
# STYLES
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
.stApp { background-color: #05070c !important; color: #f1f5f9 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #05070c; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
p, li, span, label, .stMarkdown { color: #94a3b8 !important; font-size: 15px !important; }
.brand-header { display: flex; justify-content: space-between; align-items: center; padding: 30px 0 15px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 30px; }
.shimmer-title { font-size: 28px !important; font-weight: 800 !important; background: linear-gradient(120deg, #ffffff 30%, #ff7a22 50%, #ffffff 70%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 4s linear infinite; }
@keyframes shine { to { background-position: 200% center; } }
.live-dot-de { display: inline-block; width: 6px; height: 6px; background-color: #ff5a00; border-radius: 50%; margin-right: 8px; }
.editorial-info-box { background: #0d111c; border-left: 3px solid #ff5a00; padding: 20px 24px; border-radius: 0 8px 8px 0; margin: 40px 0; font-size: 14.5px; color: #cbd5e1 !important; line-height: 1.6; }
.info-bullet-list { margin-top: 15px; padding-left: 5px; }
.info-bullet-item { margin-bottom: 12px; color: #94a3b8 !important; }
.info-bullet-item strong { color: #ffffff !important; }
[data-testid="stFileUploader"] { background: #0d111c !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 8px !important; padding: 18px !important; }
div.stDownloadButton > button { background-color: transparent !important; color: #ff5a00 !important; border: 1px solid rgba(255, 90, 0, 0.3) !important; padding: 8px 16px !important; font-size: 13.5px !important; border-radius: 4px !important; width: 100% !important; text-align: left !important; }
.clean-kpi-container { padding: 25px 0; margin: 25px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
.kpi-shimmer-number { font-size: 38px !important; font-weight: 800; background: linear-gradient(90deg, #ff5a00 0%, #ff9e66 50%, #ff5a00 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 5s linear infinite; }
.section-headline { font-size: 15px !important; font-weight: 700 !important; color: #64748b !important; text-transform: uppercase; letter-spacing: 1.5px; margin: 40px 0 15px 0; }
.news-card { background: #0d111c; border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 6px; padding: 20px; margin-bottom: 12px; }
.news-headline { font-size: 17px !important; font-weight: 600 !important; color: #ffffff !important; margin-bottom: 6px; }
.news-url-anchor { font-size: 13px !important; color: #64748b !important; text-decoration: none; }
.feedback-box { text-align: center; padding: 40px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 80px; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="brand-header">
    <div class="shimmer-title">ZDFheute 🧡 ZDF Digital <span style="color:rgba(255,255,255,0.15); font-weight:300; margin:0 8px;">|</span> WhatsApp Artikel-Checker</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUTS
# =========================================================
col_file, col_d1, col_d2 = st.columns([2, 1, 1])
with col_file: file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col_d1: start_date = st.date_input("Startdatum", value=(datetime.now() - timedelta(days=datetime.now().weekday())), format="DD.MM.YYYY")
with col_d2: end_date = st.date_input("Enddatum", value=date.today(), format="DD.MM.YYYY")

st.download_button("💡 Anleitung zum Piano-Export", "ANLEITUNG: EXCEL-EXPORT AUS PIANO ANALYTICS...", file_name="Anleitung.txt")

st.markdown("""
<div class="editorial-info-box">
    Dieses Tool gleicht ab, welche Web/App-Artikel bereits auf WhatsApp erschienen sind. 
    <div class="info-bullet-list">
        <div class="info-bullet-item"><strong>• Macht und Folgen:</strong> Politik & Analysen.</div>
        <div class="info-bullet-item"><strong>• Gut zu wissen:</strong> Service & Ratgeber.</div>
        <div class="info-bullet-item"><strong>• Zwischen Tat und Aufklärung:</strong> True Crime.</div>
        <div class="info-bullet-item"><strong>• Trends, Pop & Kurioses:</strong> Popkultur.</div>
        <div class="info-bullet-item"><strong>• Sonstige Artikel:</strong> Rest.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FUNKTIONEN
# =========================================================
def get_slug(url): return url.strip('/').split('/')[-1].split('?')[0].lower()

def should_filter_out(url):
    return any(x in url.lower() for x in ["presseportal", "video", "briefing", "thema", "phoenix", "newsticker"])

def categorize(title, url):
    t, u = title.lower(), url.lower()
    if any(x in t for x in ["mord", "polizei", "prozess", "tat", "ermittlung"]): return "Zwischen Tat und Aufklärung"
    if any(x in t for x in ["wetter", "rezept", "geld", "ratgeber", "ernährung"]): return "Gut zu wissen"
    if any(x in u for x in ["politik", "scholz", "bundestag", "krieg"]): return "Macht und Folgen"
    if any(x in t for x in ["promi", "tiktok", "viral", "film", "musik"]): return "Trends, Pop & Kurioses"
    return "Sonstige Artikel"

def get_articles_from_search(max_pages=10):
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

# =========================================================
# MAIN
# =========================================================
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

st.markdown('<div class="feedback-box">Du hast Feedback? Schreibe an <strong>Matthias Schmickl</strong>.</div>', unsafe_allow_html=True)
