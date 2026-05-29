import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


# =========================================================
# HEADER
# =========================================================
st.title("ZDFheute Whatsapp Artikel-Checker")
st.caption("by ZDF Digital News-Redaktion")

st.markdown("""
Dieses Tool überprüft anhand einer Excel-Datei, welche ZDFheute-Artikel im Zeitraum NICHT im WhatsApp-Kanal veröffentlicht wurden und ordnet sie in Themenbereiche ein.
""")


# =========================================================
# ZEITRAUM (nur UI aktuell, später erweiterbar)
# =========================================================
st.subheader("Zeitraum auswählen")

col1, col2 = st.columns(2)

start_date = col1.date_input("Von", value=datetime.today())
end_date = col2.date_input("Bis", value=datetime.today())


# =========================================================
# HARTE BLOCKLIST (BLEIBT 100% WICHTIG)
# =========================================================
BLOCK_PREFIXES = [
    "https://www.zdfheute.de/briefing",
    "https://www.zdfheute.de/thema",
    "https://www.zdfheute.de/in-eigener-sache",
    "https://www.phoenix.de",
    "https://www.zdfheute.de/video"
]


# =========================================================
# KATEGORIEN (VERFEINERT, KEINE STRUKTURÄNDERUNG)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()


    # ❌ HARTE EXKLUSION
    if any(u.startswith(x) for x in BLOCK_PREFIXES):
        return None


    # =====================================================
    # 🟦 MACHT & FOLGEN
    # =====================================================
    if u.startswith("https://www.zdfheute.de/politik"):
        return "Macht und Folgen"

    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","gesetz",
        "eu","usa","russland","china","krieg","konflikt",
        "diplomatie","analyse","einordnung","wirtschaft",
        "gipfel","nato","ukraine","nahost"
    ]):
        return "Macht und Folgen"


    # =====================================================
    # 🟩 SERVICE & ALLTAG
    # =====================================================
    if u.startswith("https://www.zdfheute.de/ratgeber"):
        return "Service & Alltag"

    if any(x in t for x in [
        "essen","rezept","ernährung","kochen","haushalt",
        "gesundheit","arzt","medizin","tipps","ratgeber",
        "geld","steuer","rente","miete","verbraucher",
        "versicherung","finanzen","spar","alltag"
    ]):
        return "Service & Alltag"


    # =====================================================
    # 🟥 KRIMINALITÄT / JUSTIZ
    # =====================================================
    if any(x in t for x in [
        "polizei","gericht","mord","tat","verbrechen",
        "prozess","urteil","ermittlung","festnahme","anschlag",
        "raub","betrug"
    ]):
        return "Zwischen Tat und Aufklärung"


    # =====================================================
    # 🟪 TRENDS & UNTERHALTUNG (PROMIS FIX!)
    # =====================================================
    if any(x in t for x in [
        # PROMI / ENTERTAINMENT (wichtig erweitert)
        "promi","star","stars","model","schauspieler","sänger",
        "musik","album","konzert","tv","fernsehen","show",
        "serie","film","kino","streaming","reality",
        "instagram","tiktok","viral","trend","social",
        "mode","fashion","gntm","germany's next topmodel",
        "royal","royals","boulevard","comeback"
    ]):
        return "Trends & Unterhaltung"


    # =====================================================
    # ⚫ SONSTIGES
    # =====================================================
    return "Sonstiges"


# =========================================================
# RSS DATEN
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

                if title_el is None or link_el is None:
                    continue

                title = title_el.text.strip()
                link = link_el.text.strip()

                u = link.lower()

                # ❌ HARTE BLOCKLIST
                if any(u.startswith(x) for x in BLOCK_PREFIXES):
                    continue

                if "video" in u:
                    continue

                if u.count("/") <= 3:
                    continue

                articles.append({
                    "title": title,
                    "url": link
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
