import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET


# =========================================================
# HEADER
# =========================================================
st.title("ZDFheute Whatsapp Artikel-Checker")
st.caption("by ZDF Digital News-Redaktion")


# =========================================================
# HARTE EXKLUSION (IMMER ZUERST!)
# =========================================================
BLOCK_PREFIXES = [
    "https://www.zdfheute.de/briefing",
    "https://www.zdfheute.de/thema",
    "https://www.zdfheute.de/in-eigener-sache",
    "https://www.zdfheute.de/video",
    "https://www.phoenix.de",
    "https://presseportal.zdf.de/pressemitteilungen",
    "https://www.zdf.de/dokus"
]


# =========================================================
# CATEGORY ENGINE (PRIORITY BASED)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()

    # =========================
    # 1. HARD EXCLUSION
    # =========================
    if any(u.startswith(x) for x in BLOCK_PREFIXES):
        return None


    # =========================
    # 2. HARD URL RULES
    # =========================

    # 🟦 POLITIK
    if "/politik" in u:
        return "Macht und Folgen"

    # 🟩 SERVICE
    if "/ratgeber" in u:
        return "Service & Alltag"

    # 🟥 PANORAMA = default society OR entertainment hybrid
    if "/panorama" in u:

        entertainment_keywords = [
            "star","stars","promi","show","musik","film","serie",
            "tv","fernsehen","konzert","mode","fashion","viral",
            "instagram","tiktok","comeback","sänger","schauspieler"
        ]

        if any(x in t for x in entertainment_keywords):
            return "Trends & Unterhaltung"

        return "Gesellschaft & Alltag"


    # =========================
    # 3. CRIME / JUSTICE
    # =========================
    if any(x in t for x in [
        "polizei","gericht","mord","tat","verbrechen",
        "prozess","urteil","ermittlung","anschlag"
    ]):
        return "Zwischen Tat und Aufklärung"


    # =========================
    # 4. SERVICE KEYWORDS FALLBACK
    # =========================
    if any(x in t for x in [
        "essen","rezept","ernährung","haushalt","gesundheit",
        "geld","steuer","rente","miete","verbraucher"
    ]):
        return "Service & Alltag"


    # =========================
    # 5. POLITICS KEYWORDS FALLBACK
    # =========================
    if any(x in t for x in [
        "politik","regierung","bundestag","wahl","krieg",
        "eu","usa","russland","china","analyse","einordnung"
    ]):
        return "Macht und Folgen"


    # =========================
    # 6. ENTERTAINMENT GLOBAL FALLBACK
    # =========================
    if any(x in t for x in [
        "promi","star","show","film","serie","musik",
        "tv","viral","trend","social","tiktok","instagram"
    ]):
        return "Trends & Unterhaltung"


    # =========================
    # 7. FALLBACK
    # =========================
    return "Sonstiges"


# =========================================================
# RSS FETCH (simplified, stable)
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
        "Macht und Folgen",
        "Service & Alltag",
        "Zwischen Tat und Aufklärung",
        "Trends & Unterhaltung",
        "Gesellschaft & Alltag",
        "Sonstiges"
    ]

    for cat in order:

        items = grouped.get(cat, [])

        if items:
            st.subheader(cat)

            for a in items:
                st.write(a["title"])
                st.write(a["url"])
