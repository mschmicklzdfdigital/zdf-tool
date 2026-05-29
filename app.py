import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import time

# [Behalte die ui_styles und header_html aus deinem vorherigen Code bei]

# =========================================================
# DYNAMISCHE KALENDERWOCHEN-LOGIK
# =========================================================
def get_last_monday():
    today = datetime.now()
    # Berechne den letzten Montag
    last_monday = today - timedelta(days=today.weekday())
    return datetime.combine(last_monday.date(), datetime.min.time())

# =========================================================
# WEB-SCRAPER FÜR DIE ZDF-SUCHE (STATT RSS)
# =========================================================
@st.cache_data(ttl=3600)
def get_articles_from_zdf_search(pages=10):
    all_articles = []
    base_url = "https://www.zdfheute.de/suche?q=*&type=all&page={}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for page in range(1, pages + 1):
        try:
            url = base_url.format(page)
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200: continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            # Selektoren für die Suchergebnisse
            items = soup.select('article.teaser-full, article.teaser-standard')
            
            for item in items:
                link_tag = item.find('a', href=True)
                headline_tag = item.find('h3') or item.find('h2')
                
                if link_tag and headline_tag:
                    title = headline_tag.get_text(strip=True)
                    link = "https://www.zdfheute.de" + link_tag['href'] if link_tag['href'].startswith('/') else link_tag['href']
                    
                    # Da die Suche keine Zeitstempel hat, nehmen wir an, 
                    # dass die Suche chronologisch ist.
                    all_articles.append({"title": title, "url": link, "datetime": datetime.now()})
            time.sleep(0.3)
        except: continue
    return all_articles

# =========================================================
# RESTLICHES SKRIPT (ADAPTIERT)
# =========================================================

# Ersetze in deiner Main-Logik den RSS-Aufruf durch:
start_datetime = get_last_monday()
end_datetime = datetime.now()

# Hinweis: Da die Suche keine exakten Zeitstempel liefert, 
# vertrauen wir auf die Aktualität der Suche.
online_articles = get_articles_from_zdf_search(pages=15) 

# [Der Rest deines Abgleich-Codes bleibt identisch]
