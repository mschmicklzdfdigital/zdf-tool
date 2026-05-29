import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


# -------------------------
# STREAMLIT MUSS ALS ERSTES FUNKTIONIEREN
# -------------------------


# -------------------------
# KATEGORIEN
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
        "gesundheit","essen","rezept","service","verbraucher","miete"
    ]):
        return "Service & Alltag"

    if any(x in t for x in [
        "polizei","tat","mord","gericht","prozess","verbrechen",
        "ermittlung","täter","opfer","unfall"
    ]):
        return "Zwischen Tat und Aufklärung"

    if any(x in t for x in [
        "trend","viral","tiktok","promi","show","musik","social",
        "internet","kino","serie","kurios"
    ]):
        return "Trends & Unterhaltung"

    return "Sonstiges"


# -------------------------
# DATENQUELLE (RSS stabil + vollständig)
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

    for feed in feeds:

        try:
            r = requests.get(feed, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)

            for item in root.findall(".//item"):

                title_el = item.find("title")
                link_el = item.find("link")

                if title_el is None or link_el is None:
                    continue

                title = title_el.text
                link = link_el.text

                if not title or not link:
                    continue

                title = title.strip()
                link = link.strip()

                # ❌ VIDEO LINKS RAUS
                if link.startswith("https://www.zdf.de/video"):
                    continue

                if "video" in title.lower():
                    continue

                # ❌ Übersichtsseiten raus
                blocked_paths = [
                    "/politik","/wirtschaft","/panorama",
                    "/sport","/gesundheit","/kultur","/doku"
                ]

                if any(link.startswith("https://www.zdf.de" + p) for p in blocked_paths):
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
st.title("ZDFheute Excel Abgleich Tool")

file = st.file_uploader("Excel hochladen (erste Spalte = Titel)")


# -------------------------
# MAIN LOGIC
# -------------------------
if file:

    df = pd.read_excel(file, engine="openpyxl")

    excel_titles = set(
        df.iloc[:, 0].astype(str).str.lower().str.strip()
    )

    articles = get_articles()

    grouped = {}

    seen = set()

    for a in articles:

        title = a["title"].lower().strip()

        # Duplikate entfernen
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
