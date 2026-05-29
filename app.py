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
# HIGH-END ORANGE CYBERPUNK THEME (2026 RADICAL DESIGN)
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Deep Orbit Background mit starkem Fokus auf Orange-Akzente */
.stApp {
    background: radial-gradient(circle at 80% 10%, rgba(255, 90, 0, 0.08) 0%, #060913 60%, #020306 100%) !important;
    color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Custom Scrollbar im glühenden Orange-Stil */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #060913; }
::-webkit-scrollbar-thumb { background: rgba(255, 90, 0, 0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #ff5a00; box-shadow: 0 0 10px #ff5a00; }

p, li, span, label, .stMarkdown {
    color: #cbd5e1 !important;
    font-size: 15px !important;
}

/* Brutalistischer, cleaner Brand-Header */
.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 0;
    border-bottom: 3px solid #ff5a00;
    margin-bottom: 35px;
    box-shadow: 0 4px 30px rgba(255, 90, 0, 0.1);
}
.main-title {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -1.5px;
}
.orange-glow-text {
    color: #ff5a00 !important;
    text-shadow: 0 0 15px rgba(255, 90, 0, 0.6);
}

/* Pulsierender deutscher Live-Status */
.live-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    background-color: #ff5a00;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 12px #ff5a00;
    animation: pulseGlow 1.5s infinite;
}
@keyframes pulseGlow {
    0% { transform: scale(0.9); opacity: 0.5; }
    50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 18px #ff5a00; }
    100% { transform: scale(0.9); opacity: 0.5; }
}

/* Ultramoderner Dateiuploader (Voller Kontrast, Orange Border) */
[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 2px solid #ff5a00 !important;
    box-shadow: 0 0 20px rgba(255, 90, 0, 0.1);
    border-radius: 12px !important;
    padding: 20px !important;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    box-shadow: 0 0 30px rgba(255, 90, 0, 0.25);
    background: rgba(255, 90, 0, 0.02) !important;
}
[data-testid="stFileUploader"] label p {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 16px !important;
}

/* Massives, fettes KPI Dashboard Centerpiece */
.center-kpi-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 2px solid rgba(255, 90, 0, 0.3);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    margin: 25px 0 40px 0;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.kpi-massive-number {
    font-size: 56px !important;
    font-weight: 900;
    color: #ff5a00 !important;
    line-height: 1;
    letter-spacing: -2px;
    filter: drop-shadow(0 0 20px rgba(255, 90, 0, 0.5));
}

/* Scharfe Kategorie-Überschriften */
.section-headline {
    font-size: 20px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
    margin: 45px 0 20px 0;
    padding-left: 14px;
    border-left: 5px solid #ff5a00;
}

/* Glow-Karten für News mit heftigem Hover-Effekt */
.news-card {
    background: rgba(20, 30, 54, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid #ff5a00;
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 16px;
    transition: all 0.35s cubic-bezier(0.25, 1, 0.5, 1);
}
.news-card:hover {
    border-left-width: 8px;
    background: linear-gradient(95deg, rgba(255, 90, 0, 0.06) 0%, rgba(20, 30, 54, 0.9) 100%);
    transform: translateX(8px);
    box-sizing: border-box;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5), 0 0 25px rgba(255, 90, 0, 0.15);
}
.news-headline {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 8px;
}
.news-url-anchor {
    font-size: 13px !important;
    color: #ffaa66 !important;
    text-decoration: none;
    font-weight: 600;
}
.news-url-anchor:hover {
    color: #ff5a00 !important;
    text-decoration: underline;
}

/* Feedback Box */
.feedback-box {
    text-align: center;
    padding: 45px;
    border: 2px dashed rgba(255, 90, 0, 0.3);
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.6);
    margin-top: 60px;
}
.feedback-title {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin-bottom: 10px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# GENERATE DYNAMIC LIVE TIMESTAMP (DEUTSCH)
# =========================================================
jetzt_de = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

# =========================================================
# BRAND HEADER
# =========================================================
header_html = f"""
<div class="brand-header">
    <div class="main-title">
        ZDFheute <span class="orange-glow-text">🧡</span> ZDF Digital <span style="color:rgba(255,255,255,0.15); font-weight:300; margin:0 12px;">|</span> WhatsApp Artikel-Checker
    </div>
    <div style="text-align: right; font-size: 12px; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">
        <span class="live-dot"></span>STATUS: <span style="color: #ff5a00;">LIVE-DATEN AKTIV</span><br>
        <span style="color: #64748b; font-weight: 500;">{jetzt_de}</span>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# =========================================================
# ERKLÄRUNGSTEXT
# =========================================================
st.markdown("""
<div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #ff5a00; border-radius: 8px; padding: 18px; margin-bottom: 40px;">
    <span style="color: #e2e8f0; font-size: 15px;">
        Dieses Tool analysiert ZDFheute-Artikel im gewählten Zeitraum, vergleicht sie mit einer 
        Excel-Liste der Artikel, die auf dem WhatsApp-Kanal der ZDFheute liefen (anhand der piano-Excel-Datei) 
        und zeigt dir nur die Inhalte, die noch nicht im WhatsApp-Kanal veröffentlicht wurden.
    </span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# KONTROLL-PANEL
# =========================================================
col_file, col_d1, col_d2 = st.columns([2, 1, 1])

with col_file:
    file = st.file_uploader("Hier Excel-Datei hochladen", type=["xlsx"])

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
    parts = [p for p in clean_url.split('/') if p]
    if len(parts) <= 2: 
        if len(parts) == 2 and parts[0] in ["zdf.de", "zdfheute.de"]: return True
    return False

def categorize(title, url):
    t = title.lower().strip()
    u = url.lower().strip()

    if "wetter" in t or "gewitter" in t or "hitzewelle" in t or "unwetter" in t or "regen" in t:
        return "Gut zu wissen"

    pop_keywords = [
        "promi", "star", "heidi", "helene", "klum", "fischer", "lindenberg", "sänger", 
        "schauspieler", "musik", "film", "serie", "show", "kino", "festival", "tiktok", 
        "instagram", "viral", "kurios", "wunder", "hype", "popstar", "bühne", "oscar"
    ]
    if "zdfheute.de/panorama/prominente" in u or any(x in t for x in pop_keywords):
        return "Trends, Pop & Kurioses"

    crime_keywords = [
        "mord", "tat", "gericht", "polizei", "kriminal", "prozess", "anklage", "festnahme", 
        "ermittlung", "fahndung", "raub", "diebstahl", "schüsse", "toter", "leiche", "opfer", 
        "täter", "haftbefehl", "sek", "clan", "drogen", "betrug", "jva", "gefängnis"
    ]
    if any(x in t for x in crime_keywords):
        return "Zwischen Tat und Aufklärung"

    if "zdfheute.de/ratgeber" in u: return "Gut zu wissen"
    
    service_keywords = [
        "essen", "rezept", "ernährung", "gesundheit", "geld", "steuer", "miete", "rente", 
        "tipps", "haushalt", "verbraucher", "krankenkasse", "gehalt", "sparen", "energie", 
        "heizung", "urlaub", "reisen", "medizin", "arzt", "verkehr", "bahn"
    ]
    if any(x in t for x in service_keywords): return "Gut zu wissen"

    if "zdfheute.de/politik" in u or "zdf.de/politik" in u: return "Macht und Folgen"
        
    analysis_keywords = [
        "analyse", "einordnung", "kommentar", "hintergrund", "erklärung", "zusammenhang", 
        "politik", "bundestag", "scholz", "habeck", "baerbock", "regierung", "wahl", "usa", 
        "trump", "biden", "china", "russland", "ukraine", "krieg", "sanktionen", "nato", "eu", 
        "nahost", "israel", "gaza", "krise", "konflikt", "strategie", "reform", "podcasts"
    ]
    if any(x in t for x in analysis_keywords): return "Macht und Folgen"

    return "Sonstige Artikel"

# =========================================================
# RSS FEED FETCHING
# =========================================================
@st.cache_data(ttl=300)
def get_articles_from_rss():
    feeds = [
        "https://www.zdf.de/rss/zdf/nachrichten",
        "https://www.zdf.de/rss/zdf/politik",
        "https://www.zdf.de/rss/zdf/wirtschaft",
        "https://www.zdf.de/rss/zdf/panorama",
        "https://www.zdf.de/rss/zdf/sport",
        "https://www.zdf.de/rss/zdf/wissen"
    ]
    fetched = []
    for feed in feeds:
        try:
            r = requests.get(feed, headers={"User-Agent": "ZDFheute Hub"}, timeout=10)
            if r.status_code != 200: continue
            root = ET.fromstring(r.content)
            for item in root.findall(".//item"):
                title = item.findtext("title")
                link = item.findtext("link")
                pub_date_str = item.findtext("pubDate")
                if not title or not link: continue
                
                if pub_date_str:
                    try:
                        clean_date_str = pub_date_str.rsplit(' ', 1)[0]
                        article_time = datetime.strptime(clean_date_str, "%a, %d %b %Y %H:%M:%S")
                    except:
                        article_time = datetime.now()
                else:
                    article_time = datetime.now()

                fetched.append({"title": title.strip(), "url": link.strip(), "datetime": article_time})
        except:
            continue
    return fetched

# =========================================================
# MAIN LIVE ENGINE PROCESSING
# =========================================================
if file:
    df = pd.read_excel(file, engine="openpyxl")
    excel_titles = set(df.iloc[:,0].astype(str).str.lower().str.strip())
    excel_urls = set()
    if df.shape[1] > 1:
        excel_urls = set(df.iloc[:,1].astype(str).str.lower().str.strip())
        
    online_articles = get_articles_from_rss()
    
    target_categories = [
        "Macht und Folgen",
        "Gut zu wissen",
        "Zwischen Tat und Aufklärung",
        "Trends, Pop & Kurioses",
        "Sonstige Artikel"
    ]
    grouped = {cat: [] for cat in target_categories}
    
    for a in online_articles:
        if not (start_datetime <= a["datetime"] <= end_datetime): continue
        if should_filter_out(a["url"]): continue
        if a["title"].lower().strip() in excel_titles or a["url"].lower().strip() in excel_urls: continue
            
        cat = categorize(a["title"], a["url"])
        grouped[cat].append(a)

    total_missing = sum(len(v) for v in grouped.values())
    
    # Der neue, ultra-fokussierte Centerpiece KPI-Block
    st.markdown(f"""
    <div class="center-kpi-box">
        <div class="kpi-massive-number">Fehlende Artikel: {total_missing}</div>
    </div>
    """, unsafe_allow_html=True)

    has_results = False
    for cat in target_categories:
        items = grouped[cat]
        if len(items) > 0:
            has_results = True
            st.markdown(f'<div class="section-headline">{cat} ({len(items)})</div>', unsafe_allow_html=True)
            for item in items:
                headline = item['title'].replace('"', '&quot;')
                url = item['url']
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-headline">{headline}</div>
                    <a href="{url}" target="_blank" class="news-url-anchor">{url}</a>
                </div>
                """, unsafe_allow_html=True)
                
    if not has_results:
        st.markdown('<div style="color:#2ed573; font-weight:600; padding:25px; background:rgba(46,213,115,0.05); border:1px solid #2ed573; border-radius:10px; text-align:center;">✔ Perfekt! Alle Artikel sind bereits im WhatsApp-Kanal vorhanden.</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="feedback-box">
        <div class="feedback-title">Du hast Feedback oder dir ist etwas aufgefallen? <span style="color:#ff5a00; filter: drop-shadow(0 0 6px #ff5a00);">🧡</span></div>
        <div class="feedback-text">Schreibe oder schicke deine Anmerkungen jederzeit direkt an <strong>Matthias Schmickl</strong>.</div>
    </div>
    """, unsafe_allow_html=True)
