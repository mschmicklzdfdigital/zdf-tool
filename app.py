import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION (PIKFEIN & PROFESSIONAL)
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Intelligence Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# NEXT-GEN CYBER SLATE & BRAND CORAL THEME
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at 50% 0%, #0d1527 0%, #050810 100%) !important;
    color: #f8fafc !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid rgba(255, 90, 0, 0.15);
    margin-bottom: 35px;
}
.brand-logos-left {
    display: flex;
    align-items: center;
    gap: 25px;
}
.brand-logo-img {
    height: 45px;
    object-fit: contain;
}
.brand-divider {
    width: 1px;
    height: 40px;
    background: rgba(255, 255, 255, 0.15);
}
.title-block {
    display: flex;
    flex-direction: column;
}
.main-title {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.8px;
    background: linear-gradient(135deg, #ffffff 40%, #ff5a00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.meta-subtitle {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-top: 2px;
}
.premium-info-wrapper {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid #ff5a00;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
}
.premium-info-text {
    font-size: 15px;
    line-height: 1.6;
    color: #cbd5e1;
    font-weight: 400;
}
.section-headline {
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
    margin: 35px 0 15px 0;
    padding-left: 12px;
    border-left: 3px solid #ff5a00;
    display: flex;
    align-items: center;
    gap: 10px;
}
.news-card {
    background: rgba(13, 22, 41, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
    backdrop-filter: blur(20px);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.news-card:hover {
    border: 1px solid rgba(255, 90, 0, 0.4);
    background: linear-gradient(90deg, rgba(255, 90, 0, 0.03) 0%, rgba(13, 22, 41, 0.6) 100%);
    transform: translateX(4px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
}
.news-headline {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
    line-height: 1.45;
}
.news-url-anchor {
    font-size: 12px;
    color: #ff5a00;
    text-decoration: none;
    font-weight: 500;
    word-break: break-all;
    opacity: 0.85;
}
.news-url-anchor:hover {
    opacity: 1;
    text-decoration: underline;
}
.dashboard-stat-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 22px;
    text-align: center;
}
.dashboard-stat-val {
    font-size: 38px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(ui_styles, unsafe_allow_html=True)

# =========================================================
# LOGO BRAND HEADER (ORIGINAL BRAND ASSETS)
# =========================================================
logo_zdf_heute = "https://upload.wikimedia.org/wikipedia/commons/4/41/Zdfheute-logo-2020.jpg"
logo_zdf_digital = "https://www.zdf-digital.com/wp-content/themes/zdfdigital/assets/images/logo.svg"

header_html = f"""
<div class="brand-header">
    <div class="brand-logos-left">
        <img src="{logo_zdf_heute}" class="brand-logo-img" alt="ZDFheute">
        
        <div class="brand-divider"></div>
        
        <img src="{logo_zdf_digital}" class="brand-logo-img" alt="ZDF Digital">
        
        <div class="brand-divider"></div>
        
        <div class="title-block">
            <div class="main-title">WhatsApp Artikel-Checker</div>
            <div class="meta-subtitle">Redaktionelles Quality Audit</div>
        </div>
    </div>
    <div style="text-align: right; font-size: 11px; color: #475569; font-weight: 500;">
        SYSTEMSTATUS: <span style="color: #2ed573; font-weight: 700;">● LIVE-DATA</span><br>
        ENGINE REVISION: 2026.8
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# =========================================================
# REQUIRED MAIN TEXT MANDATE
# =========================================================
intro_html = """
<div class="premium-info-wrapper">
    <div class="premium-info-text">
        Dieses Tool analysiert ZDFheute-Artikel im gewählten Zeitraum, vergleicht sie mit einer 
        Excel-Liste der Artikel, die auf dem WhatsApp-Kanal der ZDFheute liefen (anhand der piano-Excel-Datei) 
        und zeigt dir nur die Inhalte, die noch nicht im WhatsApp-Kanal veröffentlicht wurden.
    </div>
</div>
"""
st.markdown(intro_html, unsafe_allow_html=True)

# =========================================================
# INDUSTRIAL CONTROL GRID
# =========================================================
st.markdown("<p style='font-weight: 600; font-size: 14px; margin-bottom: 8px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;'>⚙️ Dateneinspeisung & Filter-Range</p>", unsafe_allow_html=True)

col_file, col_d1, col_d2 = st.columns([2, 1, 1])

with col_file:
    file = st.file_uploader("Piano-Excel-Datei hierher ziehen", type=["xlsx"], label_visibility="collapsed")

with col_d1:
    start_date = st.date_input("Startdatum", value=date.today(), format="DD.MM.YYYY")

with col_d2:
    end_date = st.date_input("Enddatum", value=date.today(), format="DD.MM.YYYY")

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

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
    
    # NEU: Ausschluss-Filter für Dokus und Lottozahlen
    if "zdf.de/dokumentation" in u or "zdf.de/dokus" in u:
        return True
    if "lottozahlen.zdf.de" in u:
        return True
        
    # Standard-Ausschluss-Filter
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
        
    # Homepages / Index-Seiten filtern
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
# PRODUCTION STREAM NETWORK DATA
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
# LIVE PROCESSING BLOCK
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

    # -----------------------------------------------------
    # METRICS DISPLAY PANEL
    # -----------------------------------------------------
    total_missing = sum(len(v) for v in grouped.values())
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f"""
        <div class="dashboard-stat-box" style="border-color: rgba(255, 90, 0, 0.3); background: rgba(255, 90, 0, 0.05);">
            <div class="dashboard-stat-val" style="color: #ff5a00;">{total_missing}</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-top: 2px;">Fehlende WA-Artikel</div>
        </div>
        """, unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f"""
        <div class="dashboard-stat-box">
            <div class="dashboard-stat-val" style="font-size: 24px; padding-top: 10px;">{start_date.strftime('%d.%m.%Y')}</div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-top: 10px;">Audit Start-Datum</div>
        </div>
        """, unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f"""
        <div class="dashboard-stat-box">
            <div class="dashboard-stat-val" style="font-size: 24px; padding-top: 10px;">{end_date.strftime('%d.%m.%Y')}</div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-top: 10px;">Audit End-Datum</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-bottom: 35px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # RESULT RENDER NODE
    # -----------------------------------------------------
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
        st.markdown("""
        <div style="text-align: center; padding: 45px; background: rgba(46, 213, 115, 0.03); border: 1px solid rgba(46, 213, 115, 0.15); border-radius: 8px;">
            <p style="color: #2ed573; font-size: 16px; font-weight: 600; margin-bottom: 2px;">✔ Synchronisation vollständig</p>
            <p style="color: #64748b; font-size: 13px; margin: 0;">Alle erfassten Artikel wurden bereits via WhatsApp distribuiert.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 70px; background: rgba(255, 255, 255, 0.01); border: 1px dashed rgba(255, 255, 255, 0.08); border-radius: 12px;">
        <p style="color: #ff5a00; font-size: 18px; font-weight: 600; margin-bottom: 4px;">Data Processing Engine bereit</p>
        <p style="color: #64748b; font-size: 13px;">Bitte speise die Piano-Excel-Datei ein, um den Live-Cross-Check zu starten.</p>
    </div>
    """, unsafe_allow_html=True)
