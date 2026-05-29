import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime


# =========================================================
# HEADER
# =========================================================
st.title("ZDFheute Whatsapp Artikel-Checker")
st.caption("by ZDF Digital News-Redaktion")

st.markdown("""
Dieses Tool überprüft anhand einer Excel-Datei mit geposteten Links (via piano csv-Download), welche Themen beim WhatsApp-Kanal der ZDFheute in einem bestimmten Zeitraum noch nicht veröffentlicht wurden.  
Außerdem kategorisiert das Tool sie in die bei den User*innen beliebtesten Kategorien.
""")


# =========================================================
# ZEITRAUMFILTER (ECHT AKTIV)
# =========================================================
st.subheader("Zeitraum auswählen")

col1, col2 = st.columns(2)

start_date = col1.date_input("Von", value=datetime.today())
end_date = col2.date_input("Bis", value=datetime.today())


# =========================================================
# BLOCKLIST (GLOBAL - WICHTIG)
# =========================================================
BLOCK_PREFIXES = [
    "https://www.zdfheute.de/briefing",
    "https://www.zdfheute.de/thema",
    "https://www.zdfheute.de/in-eigener-sache",
    "https://www.phoenix.de",
    "https://www.zdfheute.de/video",
    "https://www.zdfheute.de/livestream",
    "https://www.zdfheute.de/newsticker",
    "https://www.zdfheute.de/sender"
]


# =========================================================
# KATEGORIEN (URL + KEYWORD HYBRID)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()

    if any(u.startswith(b) for b in BLOCK_PREFIXES):
        return None


    # SERVICE
    if u.startswith("https://www.zdfheute.de/ratgeber"):
        return "Service & Alltag"

    if any(x in t for x in [
        "essen","rezept","ernährung","haushalt","gesundheit",
        "tipps","ratgeber","service","geld","steuer","rente",
        "miete","verbraucher"
    ]):
        return "Service & Alltag"


    # POLITIK / MACHT
    if u.startswith("https://www.zdfheute.de/politik"):
        return "Macht und Folgen"

    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","eu","usa",
        "russland","china","krieg","konflikt","analyse","einordnung"
    ]):
        return "Macht und Folgen"


    # PANORAMA = Gesellschaft (nicht Politik!)
    if u.startswith("https://www.zdfheute.de/panorama"):
        return "Gesellschaft & Alltag"

    if any(x in t for x in [
        "unfall","polizei","feuer","rettung","kriminalität",
        "gericht","mord","tat","verbrechen"
    ]):
        return "Gesellschaft & Alltag"


    # KRIMINALFÄLLE / JUSTIZ
    if any(x in t for x in [
        "ermittlung","täter","opfer","prozess","urteil","anschlag"
    ]):
        return "Zwischen Tat und Aufklärung"


    # ENTERTAINMENT
    if any(x in t for x in [
        "trend","viral","tiktok","promi","serie","film",
        "musik","show","social"
    ]):
        return "Trends & Unterhaltung"


    return "Sonstiges"


# =========================================================
# RSS + DATUM (JETZT KORREKT)
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

                title_el = item.find("title")
                link_el = item.find("link")
                date_el = item.find("pubDate")

                if title_el is None or link_el is None:
                    continue

                title = title_el.text.strip()
                link = link_el.text.strip()

                # Datum parsing
                pub_date = None
                if date_el is not None and date_el.text:
                    try:
                        pub_date = parsedate_to_datetime(date_el.text).date()
                    except:
                        pub_date = None

                # Zeitraumfilter
                if pub_date:
                    if pub_date < start_date or pub_date > end_date:
                        continue

                u = link.lower()

                if any(u.startswith(b) for b in BLOCK_PREFIXES):
                    continue

                if "video" in u:
                    continue

                if u.count("/") <= 3:
                    continue

                articles.append({
                    "title": title,
                    "url": link,
                    "date": pub_date
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

    excel_titles = set(
        df.iloc[:,0].astype(str).str.lower().str.strip()
    )

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


    # =====================================================
    # OUTPUT
    # =====================================================
    order = [
        "Macht und Folgen",
        "Gesellschaft & Alltag",
        "Service & Alltag",
        "Zwischen Tat und Aufklärung",
        "Trends & Unterhaltung",
        "Sonstiges"
    ]

    for cat in order:

        items = grouped.get(cat, [])

        if items:

            st.subheader(cat)

            for a in items:
                st.write(f"**{a['title']}**")
                st.write(a["url"])
