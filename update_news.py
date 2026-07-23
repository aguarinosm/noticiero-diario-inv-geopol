import feedparser
import json
import urllib.request
from datetime import datetime

# Fuentes 100% verificadas, robustas y especializadas en mercado
FEEDS = {
    "Política, Geopolítica y Macroeconomía": {
        "🌎 Global (ONU)": "https://news.un.org/feed/subscribe/es/news/all/rss.xml",
        "🇪🇺 Europa (DW Español)": "https://rss.dw.com/rdf/rss-sp-all",
        "🌎 América (El País)": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
        "🌏 Asia-Pacífico (CNBC)": "https://search.cnbc.com/rs/search/combinedcms/view.xml?id=19832390"
    },
    "Inversión, Finanzas y Mercados": {
        "🏦 Bancos Centrales (Investing)": "https://es.investing.com/rss/news_14.rss",
        "💶 Economía Europea (BCE)": "https://www.ecb.europa.eu/rss/press.html",
        "📈 Mercados (Yahoo Finance)": "https://finance.yahoo.com/news/rss",
        "📊 Wall Street & Global (CNBC)": "https://search.cnbc.com/rs/search/combinedcms/view.xml?id=10000664"
    }
}

def fetch_news():
    all_data = {}
    
    # TRUCO: Simulamos ser un navegador Google Chrome normal para evitar que los servidores nos bloqueen
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for section, subfeeds in FEEDS.items():
        all_data[section] = {}
        for category, url in subfeeds.items():
            try:
                # Descargamos los datos usando la "máscara"
                req = urllib.request.Request(url, headers=req_headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    feed_content = response.read()
                    
                feed = feedparser.parse(feed_content)
                entries = []
                
                # Si la fuente tiene noticias, cogemos las 5 primeras
                if feed.entries:
                    for entry in feed.entries[:5]:
                        entries.append({
                            "title": entry.title,
                            "link": entry.link,
                            "date": entry.get('published', datetime.now().strftime("%Y-%m-%d"))
                        })
                else:
                    raise Exception("Feed vacío o bloqueado")
                    
                all_data[section][category] = entries
                
            except Exception as e:
                # Si una web falla excepcionalmente, mostramos un aviso elegante en lugar de un hueco en blanco
                all_data[section][category] = [{
                    "title": "⚠️ Actualizando datos. Fuente temporalmente no disponible.",
                    "link": "#",
                    "date": datetime.now().strftime("%Y-%m-%d")
                }]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_news()
