import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
import unicodedata


# =========================================================
# PAGE CONFIG (NEU: LOOK & FEEL)
# =========================================================
st.set_page_config(
    page_title="ZDFheute WhatsApp Checker",
    layout="wide"
)


# =========================================================
# HEADER AREA (UI UPGRADE)
# =========================================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("ZDFheute Whatsapp Artikel-Checker")
    st.caption("by ZDF Digital News-Redaktion")

st.markdown("---")


# Logos (Platzhalter – kannst du jederzeit ersetzen)
logo_col1, logo_col2 = st.columns(2)

with logo_col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/ZDF_logo.svg/512px-ZDF_logo.svg.png", width=140)

with logo_col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/ZDFheute_logo.svg/512px-ZDFheute_logo.svg.png", width=140)

st.markdown("---")


# =========================================================
# DESCRIPTION
# =========================================================
st.markdown("""
Dieses Tool vergleicht eine Excel-Datei mit den im definierten Zeitraum veröffentlichten ZDFheute-Artikeln, identifiziert die Inhalte, die noch nicht im WhatsApp-Kanal erschienen sind, und ordnet sie automatisch in thematische Kategorien ein. Feedback kann gerne an Matthias Schmickl gegeben werden.
""")


# =========================================================
# UPLOAD (FIX: TEXT ENTFERNT)
# =========================================================
file = st.file_uploader("Excel hochladen")


# =========================================================
# HARTE EXKLUSION
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
# NORMALISIERUNG
# =========================================================
def normalize_text(t: str) -> str:
    if not isinstance(t, str):
        return ""
    t = t.lower().strip()
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\s]", "", t)
    return t


def normalize_url(u: str) -> str:
    if not isinstance(u, str):
        return ""
    u = u.lower().strip()
    u = u.split("?")[0]
    u = u.rstrip("/")
    return u


# =========================================================
# KATEGORIEN
# =========================================================
C_POLITICS = "Macht und Folgen"
C_SERVICE = "Service & Alltag"
C_CRIME = "Zwischen Tat und Aufklärung"
C_ENTERTAINMENT = "Trends & Unterhaltung"
C_SOCIAL = "Gesellschaft & Alltag"
C_OTHER = "Sonstiges"


# =========================================================
# KATEGORISIERUNG
# =========================================================
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

        if any(x in t for x in [
            "unfall","explosion","feuer","rettung","mord",
            "polizei","tat","anschlag","ermittlung","kriminal"
        ]):
            return C_CRIME

        if any(x in t for x in [
            "gesundheit","wetter","hitze","ernährung","geld",
            "energie","kosten","tipps","haushalt","rezept"
        ]):
            return C_SERVICE

        if any(x in t for x in [
            "promi","star","stars","heidi","helene","klum","fischer",
            "lindenberg","sänger","schauspieler","musiker","moderator",
            "film","serie","tv","show","konzert","musik",
            "instagram","tiktok","viral","trend","mode","fashion"
        ]):
            return C_ENTERTAINMENT

        return C_SOCIAL

    if any(x in t for x in [
        "polizei","gericht","mord","tat","verbrechen",
        "prozess","urteil","ermittlung","anschlag"
    ]):
        return C_CRIME

    if any(x in t for x in [
        "rezept","kochen","ernährung","gesundheit","arzt",
        "geld","steuer","rente","miete","verbraucher",
        "energie","kosten","spar"
    ]):
        return C_SERVICE

    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","eu","usa",
        "russland","china","krieg","konflikt","nato",
        "analyse","einordnung"
    ]):
        return C_POLITICS

    if any(x in t for x in [
        "promi","star","musik","film","serie","tv","show",
        "konzert","instagram","tiktok","viral","trend",
        "mode","fashion"
    ]):
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

                articles.append({
                    "title": title.strip(),
                    "url": link.strip()
                })

        except:
            continue

    return articles


# =========================================================
# MAIN
# =========================================================
if file:

    df = pd.read_excel(file, engine="openpyxl")

    excel_titles = set()
    excel_urls = set()

    for t in df.iloc[:, 0].astype(str):
        excel_titles.add(normalize_text(t))

    if df.shape[1] > 1:
        for u in df.iloc[:, 1].astype(str):
            excel_urls.add(normalize_url(u))

    articles = get_articles()

    grouped = {}
    seen = set()

    for a in articles:

        url_norm = normalize_url(a["url"])
        title_norm = normalize_text(a["title"])

        if url_norm in seen:
            continue
        seen.add(url_norm)

        if url_norm in excel_urls:
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
            st.subheader(cat)

            for a in items:
                st.write(a["title"])
                st.write(a["url"])
