import json
import asyncio
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_article_links(page):
    page.goto("https://timesofindia.indiatimes.com/")
    page.wait_for_load_state("networkidle")
    
    links = set()
    for a in page.query_selector_all("a"):
        href = a.get_attribute("href")
        if href and "/articleshow/" in href and "photostory" not in href:
            full_url = (
                href if href.startswith("http") 
                else f"https://timesofindia.indiatimes.com{href}"
            )
            links.add(full_url)
    return list(links)

def scrape_article(page, url):
    try:
        page.goto(url)
        page.wait_for_timeout(3000)  # wait for JavaScript content to load

        # Grab title
        title = page.title()

        # Try common ToI content blocks
        content_blocks = [
            "div._s30J.clearfix",  # article content container
            "div.Normal",          # fallback
            "div.article-content"  # some older templates
        ]

        article_text = ""
        for selector in content_blocks:
            blocks = page.query_selector_all(selector)
            if blocks:
                for block in blocks:
                    article_text += block.inner_text().strip() + "\n"
                break

        return {
            "url": url,
            "title": title,
            "content": article_text.strip() or "No content extracted."
        }
    except Exception as e:
        print(f"[ERROR scraping] {url}: {e}")
        return None

def main():
    print("🚀 Launching Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("🌐 Fetching article links...")
        article_links = get_article_links(page)
        print(f"🔗 Found {len(article_links)} articles.")

        scraped_articles = []
        for i, url in enumerate(article_links[:20]):  # limit for testing
            print(f"\n📰 Scraping {i+1}: {url}")
            article = scrape_article(page, url)
            if article:
                scraped_articles.append(article)

        browser.close()

        # Save to JSON
        with open("toi_articles.json", "w", encoding="utf-8") as f:
            json.dump(scraped_articles, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Done! {len(scraped_articles)} articles saved to 'toi_articles.json'")

if __name__ == "__main__":
    main()
