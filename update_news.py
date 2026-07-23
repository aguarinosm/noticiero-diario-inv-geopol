import feedparser
import json
from datetime import datetime

# Estructura de fuentes organizadas por temáticas y continentes
FEEDS = {
    "Política, Geopolítica y Macroeconomía": {
        "🌎 Global (ONU)": "https://news.un.org/feed/subscribe/es/news/all/rss.xml",
        "🇪🇺 Europa (Comisión/ONU)": "https://news.un.org/feed/subscribe/es/news/region/europe/rss.xml",
        "🌎 América (Noticias)": "https://news.un.org/feed/subscribe/es/news/region/americas/rss.xml",
        "🌏 Asia-Pacífico (Noticias)": "https://news.un.org/feed/subscribe/es/news/region/asia-pacific/rss.xml"
    },
    "Inversión, Finanzas y Mercados": {
        "🏦 Bancos Centrales (FMI)": "https://www.imf.org/en/News/RSS",
        "💶 Economía Europea (BCE)": "https://www.ecb.europa.eu/rss/press.html",
        "📈 Mercados (Yahoo Finance)": "https://finance.yahoo.com/news/rss",
        "📊 Wall Street & Global (CNBC)": "https://search.cnbc.com/rs/search/combinedcms/view.xml?id=10000664"
    }
}

def fetch_news():
    all_data = {}
    
    for section, subfeeds in FEEDS.items():
        all_data[section] = {}
        for category, url in subfeeds.items():
            try:
                feed = feedparser.parse(url)
                entries = []
                # Filtramos las 5 noticias más relevantes de cada sector
                for entry in feed.entries[:5]:
                    entries.append({
                        "title": entry.title,
                        "link": entry.link,
                        "date": entry.get('published', datetime.now().strftime("%Y-%m-%d"))
                    })
                all_data[section][category] = entries
            except Exception as e:
                all_data[section][category] = []

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_news()
