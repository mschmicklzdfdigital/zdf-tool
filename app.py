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
        "https://www.zdf.de/video",   # ❌ alles Video
    ]

    blocked_paths = [
        "/politik",
        "/wirtschaft",
        "/panorama",
        "/sport",
        "/gesundheit",
        "/kultur",
        "/doku",
        "/serien",
        "/filme",
        "/magazine"
    ]

    for feed in feeds:

        try:
            r = requests.get(feed, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)

            for item in root.findall(".//item"):

                title = item.find("title").text if item.find("title") is not None else None
                link = item.find("link").text if item.find("link") is not None else None

                if not title or not link:
                    continue

                link = link.strip()

                # -------------------------
                # ❌ 1. VIDEO LINKS KOMPLETT RAUS
                # -------------------------
                if link.startswith("https://www.zdf.de/video"):
                    continue

                if "video" in title.lower():
                    continue

                # -------------------------
                # ❌ 2. ÜBERSICHTSSEITEN RAUS
                # -------------------------
                if any(link.startswith("https://www.zdf.de" + p) for p in blocked_paths):
                    continue

                # -------------------------
                # ❌ 3. GENERELLE HUB-SEITEN RAUS
                # -------------------------
                if link.count("/") <= 3:
                    continue

                articles.append({
                    "title": title.strip(),
                    "url": link
                })

        except:
            continue

    return articles
