import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_swarajya():
    BASE_URL = "https://swarajyamag.com"
    print("\n🌐 Fetching Swarajya homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/politics") or href.startswith("/news") or "/story/" in href:
            full_url = BASE_URL + href if href.startswith("/") else href
            links.add(full_url)

    print(f"🔗 Found {len(links)} Swarajya article links.")
    articles = []

    for url in list(links)[:10]:
        try:
            print(f"📰 Swarajya: {url}")
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "No title"
            paragraphs = soup.select("div.article-container p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            articles.append({
                "url": url,
                "title": title,
                "content": content if content else "No content found."
            })

            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed Swarajya article: {e}")

    return articles

def scrape_news18():
    BASE_URL = "https://www.news18.com"
    print("\n🌐 Fetching News18 homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/news/" in href or "/politics/" in href:
            if href.startswith("/"):
                href = BASE_URL + href
            links.add(href)

    print(f"🔗 Found {len(links)} News18 article links.")
    articles = []

    for url in list(links)[:10]:
        try:
            print(f"📰 News18: {url}")
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "No title"
            paragraphs = soup.select("div.article_box p, div.story_content p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            articles.append({
                "url": url,
                "title": title,
                "content": content if content else "No content found."
            })

            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed News18 article: {e}")

    return articles

def scrape_republic():
    BASE_URL = "https://www.republicworld.com"
    print("\n🌐 Fetching Republic World homepage...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/india-news/" in href or "/politics/" in href:
            full_url = BASE_URL + href if href.startswith("/") else href
            links.add(full_url)

    print(f"🔗 Found {len(links)} Republic article links.")
    articles = []

    for url in list(links)[:10]:
        try:
            print(f"📰 Republic: {url}")
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "No title"
            paragraphs = soup.select("div.article-container p, div.story__content p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            articles.append({
                "url": url,
                "title": title,
                "content": content if content else "No content found."
            })

            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed Republic article: {e}")

    return articles

def main():
    all_articles = []
    all_articles += scrape_swarajya()
    all_articles += scrape_news18()
    all_articles += scrape_republic()

    with open("right_wing_news.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Saved {len(all_articles)} articles to 'right_wing_news.json'")

if __name__ == "__main__":
    main()
