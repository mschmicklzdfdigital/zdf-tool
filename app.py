import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Intelligence Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# HIGH-END CYBERPUNK GLASSMORPHISM THEME (2026 VISUAL AUDIT)
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global Reset & Futuristic Deep Space Background */
.stApp {
    background: radial-gradient(circle at 50% 0%, #111a2e 0%, #060913 70%, #020408 100%) !important;
    color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Custom Clean Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #060913;
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #ff5a00;
}

/* Typography Enhancements */
p, li, span, label, .stMarkdown {
    color: #cbd5e1 !important;
    font-size: 15px !important;
    line-height: 1.6;
}

/* Futuristic Header Grid */
.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 0;
    border-bottom: 1px solid rgba(255, 90, 0, 0.2);
    margin-bottom: 35px;
}
.main-title {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #ffffff 60%, #ff7a33 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Animated Pulsing Live Indicator */
.live-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: #2ed573;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 10px #2ed573;
    animation: pulseGlow 1.8s infinite;
}
@keyframes pulseGlow {
    0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 4px #2ed573; }
    50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 12px #2ed573; }
    100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 4px #2ed573; }
}

/* Premium Glassmorphism Container */
.premium-info-wrapper {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(16px) saturate(120%);
    -webkit-backdrop-filter: blur(16px) saturate(120%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid #ff5a00;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.premium-info-text {
    font-size: 15px !important;
    color: #e2e8f0 !important;
}

/* NEXT-GEN DRAG & DROP UPLOADER UI */
[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(10px);
    border: 2px dashed rgba(255, 90, 0, 0.4) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
[data-testid="stFileUploader"]:hover {
    border-color: #ff5a00 !important;
    background: rgba(255, 90, 0, 0.03) !important;
    box-shadow: 0 0 25px rgba(255, 90, 0, 0.15);
}
[data-testid="stFileUploader"] label p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: -0.3px;
}

/* Cyber Stat Boxes (KPIs) */
.stat-box {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.3s ease;
}
.stat-box:hover {
    transform: translateY(-2px);
}

/* Neon Headline Dividers */
.section-headline {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.3px;
    margin: 45px 0 20px 0;
    padding-left: 14px;
    border-left: 4px solid #ff5a00;
    text-shadow: 0 0 20px rgba(255, 90, 0, 0.2);
}

/* Ultra-Clean Glowing News Cards */
.news-card {
    background: rgba(20, 30, 54, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(12px);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.news-card:hover {
    border-color: rgba(255, 90, 0, 0.5);
    background: linear-gradient(95deg, rgba(255, 90, 0, 0.04) 0%, rgba(20, 30, 54, 0.8) 100%);
    transform: translateX(6px) translateY(-2px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 20px rgba(255, 90, 0, 0.1);
}
.news-headline {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 8px;
    line-height: 1.45;
}
.news-url-anchor {
    font-size: 13px !important;
    color: #ff9e66 !important;
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.2px;
    transition: color 0.2s ease;
}
.news-url-anchor:hover {
    color: #ff5a00 !important;
    text-decoration: underline;
}

/* Glass Feedback Footer Box */
.feedback-box {
    text-align: center;
    padding: 45px;
    border: 1px dashed rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.4);
    margin-top: 50px;
    backdrop-filter: blur(10px);
}
.feedback-title {
    color: #ffffff !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    margin-bottom: 10px;
}
.feedback-text {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

/* Hide Default Streamlit Style Clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# BRAND HEADER
# =========================================================
header_html = """
<div class="brand-header">
    <div class="main-title">
        ZDFheute <span style="color:#ff5a00; filter: drop-shadow(0 0 8px #ff5a00);">🧡</span> ZDF Digital <span style="color:rgba(255,255,255,0.15); font-weight:300; margin:0 12px;">|</span> WhatsApp Artikel-Checker
    </div>
    <div style="text-align: right; font-size: 11px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">
        ENGINE STATUS: <span class="live-dot"></span><span style="color: #2ed573; font-weight:700;">ACTIVE LIVE-DATA</span><br>
        REVISION: 2026.12 // PRODUCTION
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# =========================================================
# ERKLÄRUNGSTEXT
# =========================================================
st.markdown("""
<div class="premium-info-wrapper">
    <div class="premium-info-text">
        Dieses Tool analysiert ZDFheute-Artikel im gewählten Zeitraum, vergleicht sie mit einer 
        Excel-Liste der Artikel, die auf dem WhatsApp-Kanal der ZDFheute liefen (anhand der piano-Excel-Datei) 
        und zeigt dir nur die Inhalte, die noch nicht im WhatsApp-Kanal veröffentlicht wurden.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# KONTROLL-PANEL (CONTROL MATRIX)
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
    
    if "zdf.de/dokumentation" in u or "zdf.de/dokus" in u:
        return True
    if "lottozahlen.zdf.de" in u:
        return True
    if "zdf.de/video" in u or "zdfheute.de/video" in u or "/video/" in u:
        return True
    if "zdfheute.de/briefing" in u or "zdf.de/briefing" in u or "/briefing" in u:
        return True
    if "zdfheute.de/thema" in u or "zdf.de/thema" in u or "/thema/" in u:
        return True
    if "zdfheute.de/in-eigener-sache" in u or "zdf.de/in-eigener-sache" in u:
        return True
    if "phoenix.de" in u:
        return True
        
    clean_url = u.replace("https://", "").replace("http://", "").replace("www.", "")
    parts = [p for p in clean_url.split('/') if p]
    if len(parts) <= 2: 
        if len(parts) == 2 and parts[0] in ["zdf.de", "zdfheute.de"]:
            return True
    return False

def categorize(title, url):
    t = title.lower().strip()
    u = url.lower().strip()

    # PRIORITÄT 1: Wetter & Unwetter (strikt in Service / Gut zu wissen)
    if "wetter" in t or "gewitter" in t or "hitzewelle" in t or "unwetter" in t or "regen" in t:
        return "Gut zu wissen"

    # PRIORITÄT 2: Trends, Pop & Kurioses (Promis fangen vor Politik ab!)
    pop_keywords = [
        "promi", "star", "heidi", "helene", "klum", "fischer", "lindenberg", "sänger", 
        "schauspieler", "musik", "film", "serie", "show", "kino", "festival", "tiktok", 
        "instagram", "viral", "kurios", "wunder", "hype", "popstar", "bühne", "oscar"
    ]
    if "zdfheute.de/panorama/prominente" in u or any(x in t for x in pop_keywords):
        return "Trends, Pop & Kurioses"

    # PRIORITÄT 3: Zwischen Tat und Aufklärung (Kriminalität)
    crime_keywords = [
        "mord", "tat", "gericht", "polizei", "kriminal", "prozess", "anklage", "festnahme", 
        "ermittlung", "fahndung", "raub", "diebstahl", "schüsse", "toter", "leiche", "opfer", 
        "täter", "haftbefehl", "sek", "clan", "drogen", "betrug", "jva", "gefängnis"
    ]
    if any(x in t for x in crime_keywords):
        return "Zwischen Tat und Aufklärung"

    # PRIORITÄT 4: Gut zu wissen (Klassischer Service)
    if "zdfheute.de/ratgeber" in u:
        return "Gut zu wissen"
    
    service_keywords = [
        "essen", "rezept", "ernährung", "gesundheit", "geld", "steuer", "miete", "rente", 
        "tipps", "haushalt", "verbraucher", "krankenkasse", "gehalt", "sparen", "energie", 
        "heizung", "urlaub", "reisen", "medizin", "arzt", "verkehr", "bahn"
    ]
    if any(x in t for x in service_keywords):
        return "Gut zu wissen"

    # PRIORITÄT 5: Macht und Folgen (Politik & Weltgeschehen)
    if "zdfheute.de/politik" in u or "zdf.de/politik" in u:
        return "Macht und Folgen"
        
    analysis_keywords = [
        "analyse", "einordnung", "kommentar", "hintergrund", "erklärung", "zusammenhang", 
        "politik", "bundestag", "scholz", "habeck", "baerbock", "regierung", "wahl", "usa", 
        "trump", "biden", "china", "russland", "ukraine", "krieg", "sanktionen", "nato", "eu", 
        "nahost", "israel", "gaza", "krise", "konflikt", "strategie", "reform", "podcasts"
    ]
    if any(x in t for x in analysis_keywords):
        return "Macht und Folgen"

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
            r = requests.get(feed, headers={"User-Agent": "ZDFheute Hub Bot Framework"}, timeout=10)
            if r.status_code != 200:
                continue
            root = ET.fromstring(r.content)
            
            for item in root.findall(".//item"):
                title = item.findtext("title")
                link = item.findtext("link")
                pub_date_str = item.findtext("pubDate")
                
                if not title or not link:
                    continue
                
                article_time = None
                if pub_date_str:
                    try:
                        clean_date_str = pub_date_str.rsplit(' ', 1)[0]
                        article_time = datetime.strptime(clean_date_str, "%a, %d %b %Y %H:%M:%S")
                    except:
                        article_time = datetime.now()
                else:
                    article_time = datetime.now()

                fetched.append({
                    "title": title.strip(),
                    "url": link.strip(),
                    "datetime": article_time
                })
        except:
            continue
            
    return fetched

# =========================================================
# DATA CORE PROCESSING & UI ENGINE
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
        title_lower = a["title"].lower().strip()
        url_lower = a["url"].lower().strip()
        
        if not (start_datetime <= a["datetime"] <= end_datetime):
            continue
            
        if should_filter_out(a["url"]):
            continue
            
        if title_lower in excel_titles or url_lower in excel_urls:
            continue
            
        cat = categorize(a["title"], a["url"])
        grouped[cat].append(a)

    total_missing = sum(len(v) for v in grouped.values())
    
    # KPIs in stylischen Stat-Boxen gerendert
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f'<div class="stat-box" style="border: 1px solid rgba(255, 90, 0, 0.4); background: rgba(255, 90, 0, 0.05);"><span style="font-size:32px !important; font-weight:800; color:#ff5a00; filter: drop-shadow(0 0 10px rgba(255,90,0,0.3));">{total_missing}</span><br><span style="font-size:11px !important; color:#94a3b8; font-weight:700; letter-spacing:1px;">FEHLENDE WA-ARTIKEL</span></div>', unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f'<div class="stat-box"><span style="font-size:22px !important; font-weight:700; color:#ffffff;">{start_date.strftime("%d.%m.%Y")}</span><br><span style="font-size:11px !important; color:#64748b; font-weight:700; letter-spacing:1px; margin-top:5px; display:block;">AUDIT START</span></div>', unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f'<div class="stat-box"><span style="font-size:22px !important; font-weight:700; color:#ffffff;">{end_date.strftime("%d.%m.%Y")}</span><br><span style="font-size:11px !important; color:#64748b; font-weight:700; letter-spacing:1px; margin-top:5px; display:block;">AUDIT ENDE</span></div>', unsafe_allow_html=True)
        
    st.write("")

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
        st.markdown('<div style="color:#2ed573; font-weight:600; padding:20px; background:rgba(46,213,115,0.06); border:1px solid rgba(46,213,115,0.2); border-radius:10px; text-align:center; box-shadow: 0 0 15px rgba(46,213,115,0.05);">✔ Herausragende Arbeit! Alle Artikel wurden bereits über WhatsApp distribuiert.</div>', unsafe_allow_html=True)

else:
    # High-End Feedback-Footer im geladenen Zustand
    st.markdown("""
    <div class="feedback-box">
        <div class="feedback-title">Du hast Feedback oder dir ist etwas aufgefallen? <span style="color:#ff5a00; filter: drop-shadow(0 0 5px #ff5a00);">🧡</span></div>
        <div class="feedback-text">Schreibe oder schicke deine Anmerkungen jederzeit direkt an <strong>Matthias Schmickl</strong>.</div>
    </div>
    """, unsafe_allow_html=True)
