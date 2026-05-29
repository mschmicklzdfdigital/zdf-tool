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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

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
    margin-bottom: 25px;
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

/* Button Styling fuer den volltextigen Download-Button */
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
# MAIN INFOKASTEN MIT AKTUALISIERTEM REDAKTIONSTEXT
# =========================================================
st.markdown("""
<div class="editorial-info-box">
    Dieses Tool gleicht ab, welche Web/App-Artikel von ZDFheute bereits auf dem WhatsApp-Kanal der ZDFheute erschienen sind. Am Ende zeigt es dir nur die Artikel an, die noch nicht publiziert wurden – gefiltert nach den Kategorien, die die User*innen am meisten interessieren:
    <div class="info-bullet-list">
        <div class="info-bullet-item">
            <strong>• Macht und Folgen (Politik, Analysen & internationale Themen):</strong> Hier sammeln wir alles, was erklärt, einordnet und Zusammenhänge sichtbar macht. Ein Blick auf die Daten zeigt: Diese tiefgründigen Inhalte erzielen oft niedrigere Bounce-Rates, das heißt: Die User*innen bleiben nachweislich länger dran, wenn sie genau wissen, was sie erwartet.
        </div>
        <div class="info-bullet-item">
            <strong>• Gut zu wissen (Service, Ratgeber & Wetter):</strong> Das betrifft genau die nützlichen Service-Inhalte, die im großen Tagesupdate manchmal keinen Platz mehr finden, aber extrem verlässlich Klicks und Reichweite bringen.
        </div>
        <div class="info-bullet-item">
            <strong>• Zwischen Tat und Aufklärung (True Crime):</strong> Ein fokussierter Filter für Kriminalitätsreportagen, Prozesse und aktuelle Ermittlungen. Wir wissen: True-Crime-Artikel gehören zu den am häufigsten gelesenen Geschichten der User*innen.
        </div>
        <div class="info-bullet-item">
            <strong>• Trends, Pop & Kurioses (Popkultur, Social Media & Kurioses):</strong> Leichtere, neugiergetriebene Themen, die Trends aufgreifen oder kurios sind, dabei aber trotzdem den gewohnten erklärenden Ansatz von ZDFheute behalten.
        </div>
        <div class="info-bullet-item">
            <strong>• Sonstige Artikel:</strong> Alles, was in keine der oberen Core-Kategorien fällt, damit garantiert kein relevanter Text durchs Raster fällt.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ANLEITUNG ALS FLIEGENDER DOWNLOAD-BUTTON
# =========================================================
guide_text = """ANLEITUNG: EXCEL-EXPORT AUS PIANO ANALYTICS (WINDOWS)

1. Oeffne dein Piano-Analytics-Dashboard.
2. Navigiere zum Board "Zugriffe via WhatsApp-AT-Parameter".
3. Stelle sicher, dass der Zeitraum oben im Dashboard genau dem Bereich entspricht, den du gleich im WhatsApp-Checker pruefen moechtest (z. B. "Heute" oder "Letzte 7 Tage").
4. Scrolle nach unten zu der Haupttabelle, die alle gesendeten Artikel-Links und Ueberschriften auflistet.
5. Bewege die Maus ueber die obere rechte Ecke dieser Tabelle und klicke auf das Drei-Punkte-Menue (...).
6. Waehle aus dem Dropdown-Menue die Option "Die ersten 10.000 Zeilen dieser Tabelle herunterladen" (bzw. "Download first 10,000 rows of this table").
7. Die Datei wird nun als .csv-Datei in deinem Download-Ordner gespeichert.

DATEN SAUBER IN EXCEL IMPORTIEREN:
- Oeffne ein leeres Excel-Dokument.
- Klicke oben im Menue auf den Reiter "Daten" -> "Daten abrufen" (oder direkt auf "Aus Text/CSV").
- Waehle die heruntergeladene CSV-Datei aus und klicke auf "Importieren".
- Excel zeigt dir eine Vorschau. Achte darauf, dass der Dateiorsprung auf "UTF-8" steht (damit die Umlaute stimmen), und klicke unten auf "Laden".
- Klicke jetzt oben links auf "Datei" -> "Speichern unter", waehle als Dateityp "Excel-Arbeitsmappe (.xlsx)" und speichere sie ab."""

st.download_button(
    label="💡 Du weißt nicht, wie du die erforderliche Excel-Datei bekommst? Hier gibt's die Anleitung zum Download.",
    data=guide_text,
    file_name="Anleitung_Piano_Export.txt",
    mime="text/plain"
)

# =========================================================
# KONTROLL-PANEL MATRIZ
# =========================================================
st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
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
# EXCLUSION ENGINE & VALIDATOR (INKL. AUSSCHLUSS-FILTERN)
# =========================================================
def should_filter_out(url):
    u = url.lower().strip()
    
    # Neu angeforderte Ausschlüsse (Presseportal & Newsticker)
    if "presseportal.zdf.de" in u: return True
    if "zdfheute.de/newsticker/" in u: return True
    
    # Bestehende Ausschlüsse
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
    
    st.markdown(f"""
    <div class="clean-kpi-container">
        <div class="kpi-shimmer-number">Fehlende Artikel: {total_missing}</div>
    </div>
    """, unsafe_allow_html=True)

    has_results = False
    for cat in target_categories:
        items = grouped[cat]
        if len(items) > 0:
            has_results = True
            st.markdown(f'<div class="section-headline">{cat} // {len(items)}</div>', unsafe_allow_html=True)
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
        st.markdown('<div style="color:#2ed573; font-size:14px; font-weight:500; padding:20px 0;">✔ Alle Artikel wurden bereits über den WhatsApp-Kanal ausgespielt.</div>', unsafe_allow_html=True)

# =========================================================
# DAUERHAFTER FEEDBACK FOOTER
# =========================================================
st.markdown("""
<div class="feedback-box">
    <div class="feedback-title">Du hast Feedback oder dir ist etwas aufgefallen? <span style="color:#ff5a00;">🧡</span></div>
    <div class="feedback-text" style="margin-top:6px; font-size:13px !important; color: #64748b !important;">
        Schreibe oder schicke deine Anmerkungen jederzeit direkt an <strong>Matthias Schmickl</strong>.
    </div>
</div>
""", unsafe_allow_html=True)
