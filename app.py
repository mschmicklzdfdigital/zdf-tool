import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ZDFheute WhatsApp Artikel-Checker",
    layout="wide"
)


# =========================================================
# MODERN 2026 GLASS UI THEME
# =========================================================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #05070f);
    color: white;
    font-family: Inter, Arial;
}

/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding: 18px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* GLASS CARDS */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
    margin-bottom: 10px;
}

/* KPI */
.kpi {
    background: rgba(255,77,0,0.08);
    border: 1px solid rgba(255,77,0,0.25);
    padding: 16px;
    border-radius: 14px;
    text-align:center;
}

/* TITLE */
.title {
    font-size: 22px;
    font-weight: 700;
}

/* TAGS */
.tag {
    display:inline-block;
    padding:6px 10px;
    border-radius:20px;
    margin:4px;
    background: rgba(255,255,255,0.08);
    font-size: 12px;
}

/* BUTTON LOOK */
.stButton>button {
    background:#ff4d00;
    color:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER (ROBUST LOGOS WITH FALLBACK)
# =========================================================
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0c/ZDF_logo.svg", width=70)
    st.caption("ZDF")

with col2:
    st.markdown("<div class='title' style='text-align:center;'>ZDFheute WhatsApp Artikel-Checker</div>", unsafe_allow_html=True)

with col3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/ZDFheute_Logo_2020.svg", width=100)
    st.caption("ZDFheute")


st.caption("by ZDF Digital News-Redaktion")

st.markdown("---")


# =========================================================
# DESCRIPTION
# =========================================================
st.info("""
Dieses Tool analysiert ZDFheute-Artikel im gewählten Zeitraum,
vergleicht sie mit einer Excel-Liste und zeigt dir nur die Inhalte,
die noch NICHT im WhatsApp-Kanal veröffentlicht wurden.
""")


# =========================================================
# FILE UPLOAD (FIXED - CORE MISSING FEATURE)
# =========================================================
st.subheader("📁 Excel Upload")
file = st.file_uploader("Excel-Datei hochladen (Spalte 1 = Titel, optional Spalte 2 = URL)", type=["xlsx"])


# =========================================================
# DATE FILTER (REAL CONTROL)
# =========================================================
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Startdatum")

with col2:
    end_date = st.date_input("Enddatum")


# =========================================================
# CATEGORY ENGINE (IMPROVED PROMI + SERVICE + PANORAMA FIX)
# =========================================================
def categorize(title, url):

    t = title.lower()
    u = url.lower()

    if "/politik" in u:
        return "Macht und Folgen"

    if "/ratgeber" in u:
        return "Service & Alltag"

    # TRUE CRIME / DRAMA
    if any(x in t for x in ["mord","tat","gericht","polizei","kriminal","prozess"]):
        return "Zwischen Tat und Aufklärung"

    # PROMI / ENTERTAINMENT (FIXED PANORAMA ERROR)
    if any(x in t for x in [
        "promi","star","heidi","helene","klum","fischer","lindenberg",
        "sänger","schauspieler","musik","film","serie","show"
    ]):
        return "Trends & Unterhaltung"

    # SERVICE EXPANDED
    if any(x in t for x in [
        "essen","rezept","ernährung","gesundheit","geld","steuer",
        "miete","rente","tipps","haushalt","verbraucher"
    ]):
        return "Service & Alltag"

    if "/panorama" in u:
        return "Gesellschaft & Alltag"

    return "Sonstiges"


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

                # HARD FILTERS (IMPORTANT)
                if "/video" in u:
                    continue
                if "zdfheute.de/thema" in u:
                    continue
                if "phoenix.de" in u:
                    continue

                articles.append({
                    "title": title,
                    "url": link
                })

        except:
            continue

    return articles


# =========================================================
# MAIN
# =========================================================
if file:

    df = pd.read_excel(file, engine="openpyxl")

    excel_titles = set(df.iloc[:,0].astype(str).str.lower().str.strip())

    excel_urls = set()
    if df.shape[1] > 1:
        excel_urls = set(df.iloc[:,1].astype(str).str.lower().str.strip())

    articles = get_articles()

    grouped = {}

    for a in articles:

        title = a["title"].lower().strip()
        url = a["url"].lower().strip()

        # EXCEL MATCH CHECK
        if title in excel_titles or url in excel_urls:
            continue

        cat = categorize(title, url)

        grouped.setdefault(cat, []).append(a)


    # =========================================================
    # KPI CALC
    # =========================================================
    total_missing = sum(len(v) for v in grouped.values())
    categories = len(grouped)


    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<div class='kpi'><h2>{total_missing}</h2><p>Fehlende Artikel</p></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='kpi'><h2>{categories}</h2><p>Kategorien</p></div>", unsafe_allow_html=True)


    st.markdown("---")


    # =========================================================
    # OUTPUT
    # =========================================================
    for cat, items in grouped.items():

        st.markdown(f"### {cat}")

        for a in items:

            st.markdown(f"""
            <div class="card">
                <b>{a['title']}</b><br>
                <a href="{a['url']}" target="_blank">{a['url']}</a>
            </div>
            """, unsafe_allow_html=True)
