import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
import unicodedata


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ZDFheute WhatsApp Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ZDFheute CI THEME (APP STYLE BASE)
# =========================================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #306084;
    color: white;
    font-family: Arial, sans-serif;
}

/* HEADER STYLE */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background: #253544;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 1000;
}

/* LOGO STYLE */
.logo {
    font-size: 22px;
    font-weight: bold;
    color: white;
}

.logo span {
    color: #ff4d00;
}

/* CATEGORY BAR */
.subheader {
    margin-top: 80px;
    display: flex;
    gap: 15px;
    padding: 10px 20px;
    overflow-x: auto;
}

.category {
    background: rgba(255,255,255,0.15);
    padding: 8px 14px;
    border-radius: 20px;
    white-space: nowrap;
}

/* CARD STYLE */
.card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* LINKS */
a {
    color: #ff7a1a;
    text-decoration: none;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER (ZDFheute STYLE)
# =========================================================
st.markdown("""
<div class="header">
    <div>☰ Menü</div>
    <div class="logo">ZDF<span>heute</span></div>
    <div>★ Merkliste 🔍 Suche</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SUBHEADER (KATEGORIEN)
# =========================================================
st.markdown("""
<div class="subheader">
    <div class="category">ZDFheute</div>
    <div class="category">Iran</div>
    <div class="category">Ukraine</div>
    <div class="category">Fußball-WM</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TITEL / INFO
# =========================================================
st.markdown("## ZDFheute Whatsapp Artikel-Checker")
st.caption("by ZDF Digital News-Redaktion")

st.markdown("""
Dieses Tool vergleicht eine Excel-Datei mit den im definierten Zeitraum veröffentlichten ZDFheute-Artikeln, identifiziert die Inhalte, die noch nicht im WhatsApp-Kanal erschienen sind, und ordnet sie automatisch in thematische Kategorien ein. Feedback kann gerne an Matthias Schmickl gegeben werden.
""")


# =========================================================
# EXCLUSION RULES
# =========================================================
BLOCK_PREFIXES = [
    "https://www.zdfheute.de/briefing",
    "https://www.zdfheute.de/thema",
    "https://www.zdfheute.de/in-eigener-sache",
    "https://www.phoenix.de",
    "https://presseportal.zdf.de/pressemitteilungen",
    "https://www.zdf.de/dokus",
    "https://www.zdfheute.de/video",
    "https://www.zdf.de/video",
]


# =========================================================
# NORMALIZATION
# =========================================================
def normalize_text(t):
    if not isinstance(t, str):
        return ""
    t = t.lower().strip()
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\s]", "", t)
    return t


def normalize_url(u):
    if not isinstance(u, str):
        return ""
    return u.lower().split("?")[0].rstrip("/")


# =========================================================
# CATEGORY ENGINE
# =========================================================
C_POLITICS = "Macht und Folgen"
C_SERVICE = "Service & Alltag"
C_CRIME = "Zwischen Tat und Aufklärung"
C_ENTERTAINMENT = "Trends & Unterhaltung"
C_SOCIAL = "Gesellschaft & Alltag"
C_OTHER = "Sonstiges"


def categorize(title, url):

    t = title.lower()
    u = url.lower()

    if any(u.startswith(x) for x in BLOCK_PREFIXES):
        return None

    if "/politik" in u:
        return C_POLITICS

    if "/ratgeber" in u:
        return C_SERVICE

    if "/panorama" in u:

        if any(x in t for x in ["unfall","mord","polizei","explosion","kriminal","anschlag"]):
            return C_CRIME

        if any(x in t for x in ["gesundheit","wetter","ernährung","energie","kosten","rezept"]):
            return C_SERVICE

        if any(x in t for x in ["promi","star","heidi","helene","klum","fischer","musik","film","serie","show"]):
            return C_ENTERTAINMENT

        return C_SOCIAL

    if any(x in t for x in ["politik","krieg","nato","eu","regierung","bundestag"]):
        return C_POLITICS

    if any(x in t for x in ["rezept","gesundheit","geld","steuer","rente","verbraucher"]):
        return C_SERVICE

    if any(x in t for x in ["promi","star","musik","film","serie","show","trend"]):
        return C_ENTERTAINMENT

    return C_OTHER


# =========================================================
# RSS FETCH
# =========================================================
@st.cache_data(ttl=600)
def get_articles():

    feeds = [
        "https://www.zdf.de/rss/zdf/nachrichten",
        "https://www.zdf.de/rss/zdf/politik",
        "https://www.zdf.de/rss/zdf/wirtschaft",
        "https://www.zdf.de/rss/zdf/panorama",
        "https://www.zdf.de/rss/zdf/sport"
    ]

    articles = []

    for feed in feeds:
        try:
            r = requests.get(feed, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)

            for item in root.findall(".//item"):

                title = item.findtext("title")
                link = item.findtext("link")

                if not title or not link:
                    continue

                u = link.lower()

                if "/video" in u:
                    continue

                if any(u.startswith(x) for x in BLOCK_PREFIXES):
                    continue

                articles.append({"title": title, "url": link})

        except:
            continue

    return articles


# =========================================================
# UPLOAD
# =========================================================
file = st.file_uploader("Excel hochladen")


# =========================================================
# MAIN LOGIC
# =========================================================
if file:

    df = pd.read_excel(file, engine="openpyxl")

    excel_titles = set(normalize_text(x) for x in df.iloc[:,0].astype(str))

    excel_urls = set()
    if df.shape[1] > 1:
        excel_urls = set(normalize_url(x) for x in df.iloc[:,1].astype(str))

    articles = get_articles()

    grouped = {}
    seen = set()

    for a in articles:

        url = normalize_url(a["url"])
        title = normalize_text(a["title"])

        if url in seen:
            continue
        seen.add(url)

        if url in excel_urls:
            continue

        cat = categorize(a["title"], a["url"])

        if not cat:
            cat = C_OTHER

        grouped.setdefault(cat, []).append(a)


    order = [
        C_POLITICS,
        C_SERVICE,
        C_CRIME,
        C_ENTERTAINMENT,
        C_SOCIAL,
        C_OTHER
    ]


    for cat in order:
        items = grouped.get(cat, [])

        if items:
            st.markdown(f"## {cat}")

            for a in items:
                st.markdown(f"""
                <div class="card">
                    <b>{a['title']}</b><br>
                    <a href="{a['url']}" target="_blank">{a['url']}</a>
                </div>
                """, unsafe_allow_html=True)
