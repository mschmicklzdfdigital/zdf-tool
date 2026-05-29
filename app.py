import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET


# =========================================================
# HEADER
# =========================================================
st.title("ZDFheute Whatsapp Artikel-Checker")
st.caption("by ZDF Digital News-Redaktion")

st.markdown("""
Dieses Tool vergleicht eine Excel-Datei mit den im definierten Zeitraum veröffentlichten ZDFheute-Artikeln, identifiziert die Inhalte, die noch nicht im WhatsApp-Kanal erschienen sind, und ordnet sie automatisch in thematische Kategorien ein. Feedback kann gerne an Matthias Schmickl gegeben werden.
""")


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
    "https://www.zdf.de/video",   # <<< WICHTIG FIX
]


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
# KATEGORISIERUNG (FINAL + PROMI FIX)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()

    # 1. HARD EXCLUSION
    if any(u.startswith(x) for x in BLOCK_PREFIXES):
        return None

    # 2. POLITIK
    if "/politik" in u:
        return C_POLITICS

    # 3. RATGEBER
    if "/ratgeber" in u:
        return C_SERVICE

    # 4. PANORAMA
    if "/panorama" in u:

        if any(x in t for x in [
            "unfall","explosion","feuer","rettung","mord",
            "polizei","tat","anschlag","ermittlung","kriminal"
        ]):
            return C_CRIME

        if any(x in t for x in [
            "gesundheit","wetter","hitze","ernährung","geld",
            "energie","kosten","tipps","haushalt"
        ]):
            return C_SERVICE

        # 🔥 PROMI / ENTERTAINMENT (STRIKT ERWEITERT)
        if any(x in t for x in [
            "promi","star","stars","sänger","schauspieler",
            "musiker","moderator","model","heidi","helene",
            "klum","fischer","lindenberg",
            "film","serie","tv","show","konzert",
            "instagram","tiktok","viral","trend","mode","fashion"
        ]):
            return C_ENTERTAINMENT

        return C_SOCIAL

    # 5. CRIME GLOBAL
    if any(x in t for x in [
        "polizei","gericht","mord","tat","verbrechen",
        "prozess","urteil","ermittlung","anschlag"
    ]):
        return C_CRIME

    # 6. SERVICE GLOBAL
    if any(x in t for x in [
        "rezept","kochen","ernährung","gesundheit","arzt",
        "geld","steuer","rente","miete","verbraucher",
        "energie","kosten","spar"
    ]):
        return C_SERVICE

    # 7. POLITIK GLOBAL
    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","eu","usa",
        "russland","china","krieg","konflikt","nato",
        "analyse","einordnung"
    ]):
        return C_POLITICS

    # 8. ENTERTAINMENT GLOBAL (PROMI SICHERHEIT)
    if any(x in t for x in [
        "promi","star","musik","film","serie","tv","show",
        "konzert","instagram","tiktok","viral","trend",
        "mode","fashion","schauspiel","sänger","moderator"
    ]):
        return C_ENTERTAINMENT

    return C_SOCIAL


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

                # HARD BLOCK VIDEO (FINAL FIX)
                if "/video" in u or "zdf.de/video" in u:
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
# UPLOAD
# =========================================================
file = st.file_uploader("Excel hochladen (erste Spalte = Titel)")


# =========================================================
# MAIN
# =========================================================
if file:

    df = pd.read_excel(file, engine="openpyxl")

    excel_titles = set(df.iloc[:,0].astype(str).str.lower().str.strip())

    articles = get_articles()

    grouped = {}
    seen = set()

    for a in articles:

        title = a["title"].lower().strip()

        if title in seen:
            continue
        seen.add(title)

        if title in excel_titles:
            continue

        cat = categorize(a["title"], a["url"])

        if not cat:
            continue

        grouped.setdefault(cat, []).append(a)


    order = [
        C_POLITICS,
        C_SERVICE,
        C_CRIME,
        C_ENTERTAINMENT,
        C_SOCIAL,
        C_OTHER
    ]

    # KEINE LIMITIERUNG MEHR → ALLES AUSGEBEN
    for cat in order:
        items = grouped.get(cat, [])

        if items:
            st.subheader(cat)

            for a in items:
                st.write(a["title"])
                st.write(a["url"])
