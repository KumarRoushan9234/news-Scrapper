import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://scroll.in"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_article_links():
    print("🌐 Fetching Scroll homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()

    # Extract article links (looking for "href" in <a> tags)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/article/" in href:  # Articles usually have '/article/' in the URL
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
            "div.story-content",  # Main content container
            "article",             # Targeting the <article> tag if it exists
            "div.article-body",    # Alternative for the body of the article
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
    if not links:
        print("❌ No article links found!")
        return

    scraped = []

    for i, url in enumerate(links[:20]):  # Limit to 20 articles for now
        article = scrape_article(url)
        if article:
            scraped.append(article)
        time.sleep(1)  # Be polite and avoid getting blocked

    with open("scroll_articles.json", "w", encoding="utf-8") as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! {len(scraped)} articles saved to 'scroll_articles.json'")

if __name__ == "__main__":
    main()
