import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


# -------------------------
# KATEGORIEN (verbessert)
# -------------------------
def categorize(t):
    t = t.lower()

    if any(x in t for x in [
        "politik","krieg","wahl","regierung","eu","usa","russland",
        "china","international","analyse","einordnung","gipfel","konflikt"
    ]):
        return "Macht und Folgen"

    if any(x in t for x in [
        "ratgeber","tipps","wissen","erklärt","geld","steuer","rente",
        "gesundheit","essen","rezept","service","verbraucher","miete",
        "ernährung","haushalt","shopping"
    ]):
        return "Service & Alltag"

    if any(x in t for x in [
        "polizei","tat","mord","gericht","prozess","verbrechen",
        "ermittlung","täter","opfer","unfall","kriminal"
    ]):
        return "Zwischen Tat und Aufklärung"

    if any(x in t for x in [
        "trend","viral","tiktok","promi","show","musik","social",
        "internet","kino","serie","kurios","stars"
    ]):
        return "Trends & Unterhaltung"

    return "Sonstiges"


# -------------------------
# DATENQUELLE
# -------------------------
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

    blocked_prefixes = [
        "https://www.phoenix.de",          # ❌ PHOENIX KOMPLETT RAUS
        "https://www.zdf.de/video",        # ❌ Video raus
        "https://www.zdf.de/thema/",       # ❌ Themenseiten
        "https://www.zdf.de/newsticker/",
        "https://www.zdf.de/in-eigener-sache/",
        "https://www.zdf.de/sender/"
    ]

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

                # ❌ PHOENIX + BLOCKLIST
                if any(link.startswith(b) for b in blocked_prefixes):
                    continue

                # ❌ Video raus
                if "video" in link or "video" in title.lower():
                    continue

                # ❌ offensichtliche Hubs
                if link.count("/") <= 3:
                    continue

                articles.append({
                    "title": title,
                    "url": link
                })

        except:
            continue

    return articles


# -------------------------
# UI
# -------------------------
st.title("ZDFheute + Excel Abgleich Tool")

file = st.file_uploader("Excel hochladen (erste Spalte = Titel)")


# -------------------------
# MAIN
# -------------------------
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

        # ❌ schon in Excel
        if title in excel_titles:
            continue

        cat = categorize(title)

        if cat not in grouped:
            grouped[cat] = []

        grouped[cat].append(a)


    # -------------------------
    # OUTPUT
    # -------------------------
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
