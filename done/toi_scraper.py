import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://timesofindia.indiatimes.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_article_links():
    print("🌐 Fetching TOI homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/articleshow/" in href and "photostory" not in href:
            full_url = href if href.startswith("http") else BASE_URL + href
            links.add(full_url)
    
    print(f"🔗 Found {len(links)} article links.")
    return list(links)

def scrape_article(url):
    try:
        print(f"📰 Scraping: {url}")
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Title
        title = soup.title.string if soup.title else "No title found"

        # Try content selectors
        content = ""
        selectors = [
            "div._s30J.clearfix",   # New TOI container
            "div.Normal",           # Paragraph content
            "div.article-content"   # Legacy articles
        ]

        for selector in selectors:
            blocks = soup.select(selector)
            if blocks:
                for block in blocks:
                    content += block.get_text(strip=True) + "\n"
                break  # Stop at first match

        if not content:
            content = "No content found."

        return {
            "url": url,
            "title": title.strip(),
            "content": content.strip()
        }

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def main():
    links = get_article_links()
    scraped = []

    for i, url in enumerate(links[:20]):  # Limit to 20 articles for now
        article = scrape_article(url)
        if article:
            scraped.append(article)
        time.sleep(1)  # Be polite and avoid getting blocked

    with open("toi_articles_bs4.json", "w", encoding="utf-8") as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! {len(scraped)} articles saved to 'toi_articles_bs4.json'")

if __name__ == "__main__":
    main()
