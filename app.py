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
# BRAND THEME & MAX CONTRAST LIGHTING
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #090d16 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}
/* Maximale Lesbarkeit für alle Basistexte */
p, li, span, label, .stMarkdown {
    color: #f1f5f9 !important;
    font-size: 15px !important;
}
.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 2px solid #ff5a00;
    margin-bottom: 30px;
}
.main-title {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
}
.premium-info-wrapper {
    background: #111827;
    border-left: 4px solid #ff5a00;
    border-radius: 6px;
    padding: 18px;
    margin-bottom: 35px;
}
.premium-info-text {
    font-size: 15px !important;
    line-height: 1.6 !important;
    color: #e2e8f0 !important;
}

/* HIGH-VISIBILITY UPLOAD BUTTON FIX */
[data-testid="stFileUploader"] {
    background-color: #1e293b !important;
    border: 2px dashed #ff5a00 !important;
    border-radius: 8px !important;
    padding: 15px !important;
}
[data-testid="stFileUploader"] section {
    color: #ffffff !important;
}
[data-testid="stFileUploader"] label p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

.section-headline {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 35px 0 15px 0;
    padding-left: 10px;
    border-left: 4px solid #ff5a00;
}
.news-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 18px;
    margin-bottom: 12px;
}
.news-headline {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 6px;
}
.news-url-anchor {
    font-size: 13px !important;
    color: #ffaa66 !important;
    text-decoration: none;
    font-weight: 600;
}
.news-url-anchor:hover {
    text-decoration: underline;
}

/* FEEDBACK AREA BOX */
.feedback-box {
    text-align: center;
    padding: 40px;
    border: 2px dashed #334155;
    border-radius: 8px;
    background: #111827;
    margin-top: 20px;
}
.feedback-title {
    color: #ff5a00 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 8px;
}
.feedback-text {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# NEW TEXT-BASED BRAND HEADER
# =========================================================
header_html = """
<div class="brand-header">
    <div class="main-title">
        ZDFheute <span style="color:#ff5a00;">🧡</span> ZDF Digital <span style="color:#475569; font-weight:400; margin:0 10px;">|</span> WhatsApp Artikel-Checker
    </div>
    <div style="text-align: right; font-size: 11px; color: #94a3b8; font-weight: 600;">
        SYSTEMSTATUS: <span style="color: #2ed573;">● LIVE</span><br>
        REVISION: 2026.10
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
# KONTROLL-PANEL (MAX VISIBILITY UPLOAD)
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

    if "zdfheute.de/ratgeber" in u or "zdf.de/ratgeber" in u:
        return "Gut zu wissen"
    
    service_keywords = [
        "essen", "rezept", "ernährung", "gesundheit", "geld", "steuer", "miete", "rente", 
        "tipps", "haushalt", "verbraucher", "krankenkasse", "gehalt", "sparen", "energie", 
        "heizung", "urlaub", "reisen", "medizin", "arzt", "wetter", "verkehr", "bahn"
    ]
    if any(x in t for x in service_keywords):
        return "Gut zu wissen"

    crime_keywords = [
        "mord", "tat", "gericht", "polizei", "kriminal", "prozess", "anklage", "festnahme", 
        "ermittlung", "fahndung", "raub", "diebstahl", "schüsse", "toter", "leiche", "opfer", 
        "täter", "haftbefehl", "sek", "clan", "drogen", "betrug", "jva", "gefängnis"
    ]
    if any(x in t for x in crime_keywords):
        return "Zwischen Tat und Aufklärung"

    if "zdfheute.de/panorama" in u or "zdf.de/panorama" in u:
        return "Trends, Pop & Kurioses"
        
    pop_keywords = [
        "promi", "star", "heidi", "helene", "klum", "fischer", "lindenberg", "sänger", 
        "schauspieler", "musik", "film", "serie", "show", "kino", "festival", "tiktok", 
        "instagram", "viral", "kurios", "wunder", "hype", "popstar", "bühne", "oscar"
    ]
    if any(x in t for x in pop_keywords):
        return "Trends, Pop & Kurioses"

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
# DATA CORE PROCESSING
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
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f'<div style="background:#1e293b; padding:15px; border-radius:6px; text-align:center;"><span style="font-size:28px !important; font-weight:800; color:#ff5a00;">{total_missing}</span><br><span style="font-size:12px !important; color:#94a3b8;">FEHLENDE WA-ARTIKEL</span></div>', unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f'<div style="background:#1e293b; padding:15px; border-radius:6px; text-align:center;"><span style="font-size:20px !important; font-weight:700; color:#ffffff;">{start_date.strftime("%d.%m.%Y")}</span><br><span style="font-size:12px !important; color:#94a3b8;">START</span></div>', unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f'<div style="background:#1e293b; padding:15px; border-radius:6px; text-align:center;"><span style="font-size:20px !important; font-weight:700; color:#ffffff;">{end_date.strftime("%d.%m.%Y")}</span><br><span style="font-size:12px !important; color:#94a3b8;">ENDE</span></div>', unsafe_allow_html=True)
        
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
        st.markdown('<div style="color:#2ed573; font-weight:600; padding:20px; background:rgba(46,213,115,0.1); border-radius:6px;">✔ Alle Artikel wurden bereits auf WhatsApp geteilt.</div>', unsafe_allow_html=True)

else:
    # Der neue, maßgeschneiderte Feedback-Footer
    st.markdown("""
    <div class="feedback-box">
        <div class="feedback-title">Du hast Feedback oder dir ist etwas aufgefallen? <span style="color:#ff5a00;">🧡</span></div>
        <div class="feedback-text">Schreibe oder schicke deine Anmerkungen jederzeit direkt an <strong>Matthias Schmickl</strong>.</div>
    </div>
    """, unsafe_allow_html=True)
