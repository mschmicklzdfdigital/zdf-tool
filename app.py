import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# -------------------------
# KATEGORIEN
# -------------------------
def categorize(t):
    t = t.lower()

    if any(x in t for x in [
        "politik","krieg","wahl","regierung","usa","eu","russland",
        "china","international","analyse","einordnung","macht","konflikt","hintergrund"
    ]):
        return "Macht und Folgen"

    if any(x in t for x in [
        "ratgeber","tipps","wissen","erklärt","geld","gesundheit",
        "verbraucher","hilfe","check","so geht"
    ]):
        return "Gut zu wissen"

    if any(x in t for x in [
        "polizei","tat","mord","gericht","unfall","prozess",
        "verbrechen","täter","opfer","ermittlung"
    ]):
        return "Zwischen Tat und Aufklärung"

    if any(x in t for x in [
        "trend","viral","tiktok","promi","show",
        "musik","social","internet","kurios"
    ]):
        return "Trends & Kurioses"

    return None


# -------------------------
# ZDF SCRAPER (verbessert)
# -------------------------
@st.cache_data(ttl=300)
def get_zdf_articles():

    url = "https://www.zdfheute.de/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")

    articles = []

    for a in soup.find_all("a", href=True):

        title = a.get_text(strip=True)
        link = a["href"]

        if len(title) < 10:
            continue

        # ❌ VIDEO FILTER
        if "video" in title.lower() or "video" in link.lower():
            continue

        # URL fix
        if link.startswith("/"):
            link = "https://www.zdfheute.de" + link

        if "zdf" not in link:
            continue

        articles.append({
            "title": title.strip(),
            "url": link,
            "time": datetime.utcnow()
        })

    return articles


# -------------------------
# UI
# -------------------------
st.title("ZDFheute Excel Abgleich Tool")

file = st.file_uploader("Excel hochladen (erste Spalte = Titel)")

days = st.slider("Zeitraum (letzte Tage)", 1, 14, 3)


# -------------------------
# MAIN LOGIC
# -------------------------
if file:

    df = pd.read_excel(file)
    excel_titles = set(
        df.iloc[:, 0].astype(str).str.lower().str.strip()
    )

    cutoff = datetime.utcnow() - timedelta(days=days)

    articles = get_zdf_articles()

    grouped = {
        "Macht und Folgen": [],
        "Gut zu wissen": [],
        "Zwischen Tat und Aufklärung": [],
        "Trends & Kurioses": []
    }

    seen = set()

    for a in articles:

        title = a["title"].lower().strip()

        # ❌ doppelt raus
        if title in seen:
            continue
        seen.add(title)

        # ❌ schon in Excel
        if title in excel_titles:
            continue

        # ❌ Zeitraum
        if a["time"] < cutoff:
            continue

        cat = categorize(title)

        # ❌ nicht relevante Inhalte raus
        if not cat:
            continue

        grouped[cat].append(a)

    # -------------------------
    # OUTPUT
    # -------------------------
    for cat, items in grouped.items():

        if items:
            st.subheader(cat)

            for a in items:
                st.write(f"**{a['title']}**")
                st.write(a["url"])
