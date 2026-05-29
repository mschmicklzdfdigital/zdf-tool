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
# CSS STYLES (UNVERÄNDERT)
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
# HEADER & UPLOAD
# =========================================================
st.markdown("""<div class="brand-header"><div class="shimmer-title">ZDFheute 🧡 WhatsApp Artikel-Checker</div></div>""", unsafe_allow_html=True)

col_file, col_d1, col_d2 = st.columns([2, 1, 1])
with col_file: file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col_d1: start_date = st.date_input("Startdatum", value=(datetime.now() - timedelta(days=datetime.now().weekday())), format="DD.MM.YYYY")
with col_d2: end_date = st.date_input("Enddatum", value=date.today(), format="DD.MM.YYYY")

# =========================================================
# SUCH-LOGIK (DIE NEUE ENGINE)
# =========================================================
def get_articles_from_search(max_pages=20):
    all_articles = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for page in range(1, max_pages + 1):
        url = f"https://www.zdfheute.de/suche?q=*&type=all&page={page}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            # Hier greifen wir die Artikel-Teaser ab
            items = soup.select('div.teaser-full__body, div.teaser-standard__body')
            for item in items:
                link_tag = item.find('a', href=True)
                title_tag = item.find(['h2', 'h3'], class_=['teaser-full__headline', 'teaser-standard__headline'])
                if link_tag and title_tag:
                    all_articles.append({
                        "title": title_tag.get_text(strip=True),
                        "url": "https://www.zdfheute.de" + link_tag['href'] if link_tag['href'].startswith('/') else link_tag['href'],
                        "datetime": datetime.now() # Fallback, da die Suche kein exaktes Datum gibt
                    })
        except: continue
        time.sleep(0.3)
    return all_articles

# [Restliche Funktionen (should_filter_out, categorize) wie bisher behalten]

# =========================================================
# MAIN LOGIK
# =========================================================
if file:
    df = pd.read_excel(file, engine="openpyxl")
    excel_urls = set(df.iloc[:,1].astype(str).str.lower().str.strip()) if df.shape[1] > 1 else set()
    
    # Holen der Daten über Suche
    online_articles = get_articles_from_search()
    
    target_categories = ["Macht und Folgen", "Gut zu wissen", "Zwischen Tat und Aufklärung", "Trends, Pop & Kurioses", "Sonstige Artikel"]
    grouped = {cat: [] for cat in target_categories}
    
    for a in online_articles:
        if a["url"].lower().strip() in excel_urls: continue
        if should_filter_out(a["url"]): continue
        cat = categorize(a["title"], a["url"])
        grouped[cat].append(a)

    total_missing = sum(len(v) for v in grouped.values())
    st.markdown(f'<div class="clean-kpi-container"><div class="kpi-shimmer-number">Fehlende Artikel: {total_missing}</div></div>', unsafe_allow_html=True)
    
    for cat in target_categories:
        if grouped[cat]:
            st.markdown(f'<div class="section-headline">{cat} // {len(grouped[cat])}</div>', unsafe_allow_html=True)
            for item in grouped[cat]:
                st.markdown(f'<div class="news-card"><div class="news-headline">{item["title"]}</div><a href="{item["url"]}" target="_blank" class="news-url-anchor">{item["url"]}</a></div>', unsafe_allow_html=True)

# [Feedback Footer bleibt wie gehabt]
