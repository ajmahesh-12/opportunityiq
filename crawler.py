import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import json
import csv
import re
import sys

MAX_PAGES = 100

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_page(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if "text/html" not in r.headers.get("Content-Type", ""):
            return None
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        meta = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta = meta_tag.get("content", "")

        text = clean_text(soup.get_text(" ", strip=True))

        links = []
        for a in soup.find_all("a", href=True):
            links.append(a["href"])

        return {
            "url": url,
            "title": title,
            "meta_description": meta,
            "text": text,
            "links": links
        }
    except Exception as e:
        print(f"Error: {url} -> {e}")
        return None

def crawl(start_url):
    domain = urlparse(start_url).netloc
    queue = deque([start_url])
    visited = set()
    pages = []

    while queue and len(visited) < MAX_PAGES:
        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        page = extract_page(url)
        if not page:
            continue

        pages.append(page)

        for href in page["links"]:
            full = urljoin(url, href)
            parsed = urlparse(full)

            if parsed.netloc == domain:
                clean = parsed.scheme + "://" + parsed.netloc + parsed.path
                if clean not in visited:
                    queue.append(clean)

    return pages

def save_json(pages):
    with open("crawl_results.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

def save_csv(pages):
    with open("crawl_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "title", "meta_description", "text"])
        for p in pages:
            writer.writerow([
                p["url"],
                p["title"],
                p["meta_description"],
                p["text"]
            ])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawler.py https://example.com")
        sys.exit(1)

    start_url = sys.argv[1]
    pages = crawl(start_url)

    save_json(pages)
    save_csv(pages)

    print(f"Crawled {len(pages)} pages")
    print("Saved crawl_results.json")
    print("Saved crawl_results.csv")
