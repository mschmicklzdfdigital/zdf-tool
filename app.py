import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET


# =========================================================
# KATEGORIEN (verbessert + URL-Logik + saubere Trennung)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()


    # =====================================================
    # ❌ HARTE EXKLUSIONEN (kommen NIE rein)
    # =====================================================

    blocked_prefixes = [
        "https://www.zdfheute.de/briefing",
        "https://www.zdfheute.de/thema",
        "https://www.zdfheute.de/in-eigener-sache"
    ]

    if any(u.startswith(b) for b in blocked_prefixes):
        return None


    # =====================================================
    # SERVICE (URL PRIORITÄT)
    # =====================================================
    if u.startswith("https://www.zdfheute.de/ratgeber"):
        return "Service & Alltag"


    if any(x in t for x in [
        "ratgeber","tipps","wissen","erklärt","hilfe",
        "essen","rezept","ernährung","haushalt","gesundheit",
        "geld","steuer","rente","miete","verbraucher"
    ]):
        return "Service & Alltag"


    # =====================================================
    # POLITIK / MACHT / INTERNATIONAL
    # =====================================================
    if u.startswith("https://www.zdfheute.de/politik"):
        return "Macht und Folgen"


    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","gesetz",
        "eu","usa","russland","china","krieg","konflikt",
        "international","analyse","einordnung","diplomatie"
    ]):
        return "Macht und Folgen"


    # =====================================================
    # PANORAMA = NICHT POLITIK (wichtig korrigiert)
    # =====================================================
    if u.startswith("https://www.zdfheute.de/panorama"):
        return "Gesellschaft & Alltag"


    if any(x in t for x in [
        "unfall","feuer","rettung","polizei","kriminalität",
        "gericht","mord","tat","verbrechen"
    ]):
        return "Gesellschaft & Alltag"


    # =====================================================
    # TAT / KRIMINALFÄLLE (tiefer spezialisiert)
    # =====================================================
    if any(x in t for x in [
        "ermittlung","täter","opfer","prozess","urteil",
        "anschlag","festnahme"
    ]):
        return "Zwischen Tat und Aufklärung"


    # =====================================================
    # TREND / ENTERTAINMENT
    # =====================================================
    if any(x in t for x in [
        "trend","viral","tiktok","promi","show","musik",
        "serie","film","kino","social","kurios"
    ]):
        return "Trends & Unterhaltung"


    # =====================================================
    # FALLBACK
    # =====================================================
    return "Sonstiges"


# =========================================================
# DATENQUELLE
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

                # =================================================
                # ❌ HARTE EXKLUSIONEN
                # =================================================
                if any(u.startswith(b) for b in [
                    "https://www.zdfheute.de/briefing",
                    "https://www.zdfheute.de/thema",
                    "https://www.zdfheute.de/in-eigener-sache"
                ]):
                    continue

                # ❌ Videos raus
                if "video" in u:
                    continue

                # ❌ reine Navigationsseiten
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
# UI
# =========================================================
st.title("ZDFheute Excel Abgleich Tool (Final Clean Version)")

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
