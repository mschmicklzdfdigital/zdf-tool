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
# UI STYLES
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
.stApp { background-color: #05070c !important; color: #f1f5f9 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
.brand-header { display: flex; justify-content: space-between; align-items: center; padding: 30px 0 15px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 30px; }
.shimmer-title { font-size: 28px !important; font-weight: 800 !important; letter-spacing: -1.2px; background: linear-gradient(120deg, #ffffff 30%, #ff7a22 50%, #ffffff 70%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 4s linear infinite; }
@keyframes shine { to { background-position: 200% center; } }
.editorial-info-box { background: #0d111c; border-left: 3px solid #ff5a00; padding: 20px 24px; border-radius: 0 8px 8px 0; margin: 40px 0; font-size: 14.5px; color: #cbd5e1 !important; line-height: 1.6; }
.info-bullet-list { margin-top: 15px; padding-left: 5px; }
.info-bullet-item { margin-bottom: 12px; color: #94a3b8 !important; }
.info-bullet-item strong { color: #ffffff !important; }
.kpi-shimmer-number { font-size: 38px !important; font-weight: 800; background: linear-gradient(90deg, #ff5a00 0%, #ff9e66 50%, #ff5a00 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 5s linear infinite; }
.section-headline { font-size: 15px !important; font-weight: 700 !important; color: #64748b !important; text-transform: uppercase; letter-spacing: 1.5px; margin: 40px 0 15px 0; }
.news-card { background: #0d111c; border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 6px; padding: 20px; margin-bottom: 12px; }
.news-headline { font-size: 17px !important; font-weight: 600 !important; color: #ffffff !important; margin-bottom: 6px; }
.news-url-anchor { font-size: 13px !important; color: #64748b !important; text-decoration: none; }
.feedback-box { text-align: center; padding: 60px 20px; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 80px; background: rgba(255, 255, 255, 0.02); }
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="brand-header"><div class="shimmer-title">ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker</div></div>', unsafe_allow_html=True)

# =========================================================
# INPUTS & ANLEITUNG
# =========================================================
col_file, col_d1, col_d2 = st.columns([2, 1, 1])
with col_file: file = st.file_uploader("Piano-Excel-Datei hier hochladen", type=["xlsx"])
with col_d1: start_date = st.date_input("Startdatum", value=datetime.now() - timedelta(days=7))
with col_d2: end_date = st.date_input("Enddatum", value=date.today())

guide = """ANLEITUNG FÜR DEN PIANO-EXPORT:
1. Öffne das Piano-Analytics-Dashboard.
2. Navigiere zum Board 'Zugriffe via WhatsApp-AT-Parameter'.
3. Scrolle zur Tabelle mit den Artikeln.
4. Klicke oben rechts im Tabellen-Menü auf (...) und wähle 'Die ersten 10.000 Zeilen herunterladen'.
5. Importiere die CSV in Excel, speichere sie als .xlsx-Datei und lade sie hier hoch."""
st.download_button("💡 Hilfe: Wie komme ich an die Piano-Daten?", guide, file_name="anleitung.txt")

# =========================================================
# EDITORIALER KATEGORIEN-KASTEN (AUSFÜHRLICH)
# =========================================================
st.markdown("""
<div class="editorial-info-box">
    Dieses Tool gleicht ab, welche Web/App-Artikel von ZDFheute bereits auf dem WhatsApp-Kanal der ZDFheute erschienen sind. Am Ende zeigt es dir nur die Artikel an, die noch nicht publiziert wurden – gefiltert nach den Kategorien, die die User*innen am meisten interessieren:
    <div class="info-bullet-list">
        <div class="info-bullet-item"><strong>• Macht und Folgen (Politik, Analysen & internationale Themen):</strong> Hier sammeln wir alles, was erklärt, einordnet und Zusammenhänge sichtbar macht. Ein Blick auf die Daten zeigt: Diese tiefgründigen Inhalte erzielen oft niedrigere Bounce-Rates, das heißt: Die User*innen bleiben nachweislich länger dran, wenn sie genau wissen, was sie erwartet.</div>
        <div class="info-bullet-item"><strong>• Gut zu wissen (Service, Ratgeber & Wetter):</strong> Das betrifft genau die nützlichen Service-Inhalte, die im großen Tagesupdate manchmal keinen Platz mehr finden, aber extrem verlässlich Klicks und Reichweite bringen.</div>
        <div class="info-bullet-item"><strong>• Zwischen Tat und Aufklärung (True Crime):</strong> Ein fokussierter Filter für Kriminalitätsreportagen, Prozesse und aktuelle Ermittlungen. Wir wissen: True-Crime-Artikel gehören zu am häufigsten gelesenen Geschichten der User*innen.</div>
        <div class="info-bullet-item"><strong>• Trends, Pop & Kurioses (Popkultur, Social Media & Kurioses):</strong> Leichtere, neugiergetriebene Themen, die Trends aufgreifen oder kurios sind, dabei aber trotzdem den gewohnten erklärenden Ansatz von ZDFheute behalten.</div>
        <div class="info-bullet-item"><strong>• Sonstige Artikel:</strong> Alles, was in keine der oberen Core-Kategorien fällt, damit garantiert kein relevanter Text durchs Raster fällt.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LOGIK
# =========================================================
def get_slug(url): return url.strip('/').split('/')[-1].split('?')[0].lower()

def get_articles_from_search():
    all_articles = []
    for offset in range(0, 200, 20): 
        url = f"https://www.zdfheute.de/suche?q=*&type=article&from={offset}&size=20"
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            items = soup.select('div.teaser-full__body, div.teaser-standard__body')
            if not items: break 
            for item in items:
                link = item.find('a', href=True)
                title = item.find(['h2', 'h3'], class_=['teaser-full__headline', 'teaser-standard__headline'])
                if link and title:
                    full_url = "https://www.zdfheute.de" + link['href'] if link['href'].startswith('/') else link['href']
                    all_articles.append({"title": title.get_text(strip=True), "url": full_url})
        except: break
        time.sleep(0.3)
    return all_articles

if file:
    df = pd.read_excel(file, engine="openpyxl")
    excel_slugs = {get_slug(str(url)) for url in df.iloc[:,1].dropna()}
    online_articles = get_articles_from_search()
    
    grouped = {"Macht und Folgen": [], "Gut zu wissen": [], "Zwischen Tat und Aufklärung": [], "Trends, Pop & Kurioses": [], "Sonstige Artikel": []}
    
    for a in online_articles:
        if get_slug(a["url"]) in excel_slugs or any(x in a["url"].lower() for x in ["presseportal", "video", "thema"]): continue
        
        t = a["title"].lower()
        if any(x in t for x in ["mord", "polizei", "prozess", "tat", "kriminal"]): cat = "Zwischen Tat und Aufklärung"
        elif any(x in t for x in ["wetter", "rezept", "geld", "ratgeber", "ernährung"]): cat = "Gut zu wissen"
        elif "politik" in a["url"].lower() or any(x in t for x in ["scholz", "bundestag"]): cat = "Macht und Folgen"
        elif any(x in t for x in ["promi", "tiktok", "viral", "film", "kurios"]): cat = "Trends, Pop & Kurioses"
        else: cat = "Sonstige Artikel"
        grouped[cat].append(a)

    total = sum(len(v) for v in grouped.values())
    st.markdown(f'<div class="kpi-shimmer-number">Fehlende Artikel: {total}</div>', unsafe_allow_html=True)
    
    for cat, items in grouped.items():
        if items:
            st.markdown(f'<div class="section-headline">{cat}</div>', unsafe_allow_html=True)
            for item in items:
                st.markdown(f'<div class="news-card"><div class="news-headline">{item["title"]}</div><a href="{item["url"]}" target="_blank" class="news-url-anchor">{item["url"]}</a></div>', unsafe_allow_html=True)

# =========================================================
# FEEDBACK FOOTER (AUSFÜHRLICH & HÖFLICH)
# =========================================================
st.markdown("""
<div class="feedback-box">
    <h3 style="color: #ffffff;">Helfen Sie uns, noch besser zu werden! 🧡</h3>
    <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
        Dieses Tool lebt von Ihrer täglichen Arbeit. Sollten Sie Verbesserungsvorschläge haben, neue Kategorien benötigen oder ist Ihnen ein Fehler in der Anzeige aufgefallen? 
        Wir freuen uns sehr über Ihr direktes Feedback. Zögern Sie nicht, Ihre Anmerkungen jederzeit an <strong>Matthias Schmickl</strong> zu senden. 
        Vielen Dank für Ihre Unterstützung bei der stetigen Optimierung unserer Workflows!
    </p>
</div>
""", unsafe_allow_html=True)
