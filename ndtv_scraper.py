import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.ndtv.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Function to fetch NDTV homepage and get article links
def get_article_links():
    print("Fetching NDTV homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        
        if href.startswith("/india") or href.startswith("/world") or href.startswith("/sports") or href.startswith("/business"):
            full_url = href if href.startswith("http") else BASE_URL + href
            links.add(full_url)
    
    print(f"Found {len(links)} article links.")
    return list(links)

def scrape_article(url):
    try:
        print(f"Scraping: {url}")
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Title
        title = soup.title.string if soup.title else "No title found"

        # Try content selectors
        content = ""
        selectors = [
            "div.story-detail",   # Main article content
            "div.article-content",  # Legacy articles
            "div.news_story"  # Alternative content
        ]

        for selector in selectors:
            blocks = soup.select(selector)
            if blocks:
                for block in blocks:
                    content += block.get_text(strip=True) + "\n"
                break  # Stop at first match

        if not content:
            content = "No content found."

        # Additional details like timestamp, image, etc.
        timestamp = ""
        timestamp_tag = soup.find("span", class_="posted-on")
        if timestamp_tag:
            timestamp = timestamp_tag.get_text(strip=True)

        image_url = ""
        img_tag = soup.find("img")
        if img_tag:
            image_url = img_tag['src']

        return {
            "url": url,
            "title": title.strip(),
            "content": content.strip(),
            "timestamp": timestamp,
            "image_url": image_url
        }

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def main():
    links = get_article_links()
    if not links:
        print("No article links found!")
        return

    scraped = []

    for i, url in enumerate(links[:20]):  # Limit to 20 articles for now
        article = scrape_article(url)
        if article:
            scraped.append(article)
        time.sleep(1)  # Be polite and avoid getting blocked

    with open("ndtv_articles.json", "w", encoding="utf-8") as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(scraped)} articles saved to 'ndtv_articles.json'")

if __name__ == "__main__":
    main()
