import feedparser
import json
from datetime import datetime

# Fuentes oficiales RSS (FMI, ONU, Banco Central Europeo...)
FEEDS = {
    "Macroeconomía Global (FMI)": "https://www.imf.org/en/News/RSS",
    "Geopolítica Global (ONU)": "https://news.un.org/feed/subscribe/es/news/all/rss.xml",
    "Economía Europea (BCE)": "https://www.ecb.europa.eu/rss/press.html"
}

def fetch_news():
    all_news = {}
    for category, url in FEEDS.items():
        feed = feedparser.parse(url)
        entries = []
        # Cogemos las 6 noticias más importantes de cada fuente
        for entry in feed.entries[:6]: 
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.get('published', datetime.now().strftime("%Y-%m-%d"))
            })
        all_news[category] = entries
    
    # Guardamos los datos en un archivo que leerá nuestra web
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_news()
