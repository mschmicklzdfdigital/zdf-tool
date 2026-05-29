import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup


# -------------------------
# Kategorien
# -------------------------
def categorize(t):

    t = t.lower()

    if any(x in t for x in ["politik","krieg","wahl","regierung","usa","eu","russland","china","international","analyse","einordnung","macht"]):
        return "Macht und Folgen"

    if any(x in t for x in ["ratgeber","tipps","wissen","erklärt","verbraucher","gesundheit","geld","hilfe"]):
        return "Gut zu wissen"

    if any(x in t for x in ["polizei","tat","mord","gericht","unfall","prozess","verbrechen","ermittlung"]):
        return "Zwischen Tat und Aufklärung"

    if any(x in t for x in ["trend","viral","tiktok","promi","show","musik","social","internet"]):
        return "Trends & Kurioses"

    return None


# -------------------------
# ZDF SCRAPER
# -------------------------
def scrape():
    url = "https://www.zdfheute.de/"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")

    articles = []

    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        link = a["href"]

        if len(title) < 10:
            continue

        if link.startswith("/"):
            link = "https://www.zdfheute.de" + link

        if "zdfheute.de" not in link:
            continue

        articles.append({"title": title, "url": link})

    return articles


# -------------------------
# UI
# -------------------------
st.title("ZDFheute Excel Abgleich Tool")

file = st.file_uploader("Excel hochladen (erste Spalte = Titel)")

if file:

    df = pd.read_excel(file)
    excel_titles = set(df.iloc[:,0].astype(str).str.lower().str.strip())

    zdf = scrape()

    grouped = {
        "Macht und Folgen": [],
        "Gut zu wissen": [],
        "Zwischen Tat und Aufklärung": [],
        "Trends & Kurioses": []
    }

    for a in zdf:

        title = a["title"].lower().strip()

        if title in excel_titles:
            continue

        cat = categorize(title)
        if not cat:
            continue

        grouped[cat].append(a)


    for cat, items in grouped.items():

        if items:
            st.subheader(cat)

            for a in items:
                st.write(f"**{a['title']}**")
                st.write(a["url"])