import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import xml.etree.ElementTree as ET
import json
import csv
import re

MAX_PAGES = 200

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

visited = set()


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def get_domain(url):
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc


# --------------------------------------------------
# Sitemap Discovery
# --------------------------------------------------

def discover_sitemaps(base_url):

    discovered = []

    robots_url = get_domain(base_url) + "/robots.txt"

    try:
        r = requests.get(
            robots_url,
            timeout=10,
            headers=HEADERS
        )

        if r.status_code == 200:

            for line in r.text.splitlines():

                if line.lower().startswith("sitemap:"):
                    sitemap = line.split(":", 1)[1].strip()
                    discovered.append(sitemap)

    except:
        pass

    common = [
        "/sitemap.xml",
        "/sitemap_index.xml"
    ]

    for path in common:

        test_url = get_domain(base_url) + path

        if test_url not in discovered:

            try:

                r = requests.get(
                    test_url,
                    timeout=10,
                    headers=HEADERS
                )

                if r.status_code == 200:
                    discovered.append(test_url)

            except:
                pass

    return list(set(discovered))


# --------------------------------------------------
# Parse Sitemap
# --------------------------------------------------

def parse_sitemap(url):

    urls = []

    try:

        r = requests.get(
            url,
            timeout=20,
            headers=HEADERS
        )

        root = ET.fromstring(r.content)

        namespace = {
            "ns": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }

        if root.tag.endswith("sitemapindex"):

            for sitemap in root.findall(
                "ns:sitemap",
                namespace
            ):

                loc = sitemap.find(
                    "ns:loc",
                    namespace
                )

                if loc is not None:
                    urls.extend(
                        parse_sitemap(loc.text)
                    )

        elif root.tag.endswith("urlset"):

            for url_tag in root.findall(
                "ns:url",
                namespace
            ):

                loc = url_tag.find(
                    "ns:loc",
                    namespace
                )

                if loc is not None:
                    urls.append(loc.text)

    except Exception as e:

        print("Sitemap error:", url, e)

    return urls


# --------------------------------------------------
# Page Classification
# --------------------------------------------------

def classify_url(url):

    u = url.lower()

    if "/contact" in u:
        return "contact"

    if "/about" in u:
        return "about"

    if "/service" in u:
        return "service"

    if "/product" in u:
        return "product"

    if "/location" in u:
        return "location"

    if "/blog" in u:
        return "blog"

    if "/faq" in u:
        return "faq"

    return "other"


# --------------------------------------------------
# Extract Page
# --------------------------------------------------

def extract_page(url):

    try:

        r = requests.get(
            url,
            timeout=20,
            headers=HEADERS
        )

        if "text/html" not in r.headers.get(
            "Content-Type",
            ""
        ):
            return None

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        for tag in soup(
            ["script", "style", "noscript"]
        ):
            tag.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        meta = ""

        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_tag:
            meta = meta_tag.get(
                "content",
                ""
            )

        headings = []

        for h in soup.find_all(
            ["h1", "h2", "h3"]
        ):
            headings.append(
                h.get_text(strip=True)
            )

        text = clean_text(
            soup.get_text(
                " ",
                strip=True
            )
        )

        return {
            "url": url,
            "page_type": classify_url(url),
            "title": title,
            "meta_description": meta,
            "headings": headings,
            "text": text[:50000]
        }

    except Exception as e:

        print("Page error:", url, e)

        return None


# --------------------------------------------------
# Fallback Link Crawl
# --------------------------------------------------

def crawl_links(start_url):

    domain = urlparse(start_url).netloc

    queue = deque([start_url])

    urls = []

    local_visited = set()

    while queue and len(urls) < MAX_PAGES:

        current = queue.popleft()

        if current in local_visited:
            continue

        local_visited.add(current)

        try:

            r = requests.get(
                current,
                timeout=15,
                headers=HEADERS
            )

            soup = BeautifulSoup(
                r.text,
                "html.parser"
            )

            urls.append(current)

            for a in soup.find_all(
                "a",
                href=True
            ):

                href = urljoin(
                    current,
                    a["href"]
                )

                parsed = urlparse(href)

                if parsed.netloc == domain:

                    clean = (
                        parsed.scheme
                        + "://"
                        + parsed.netloc
                        + parsed.path
                    )

                    if clean not in local_visited:
                        queue.append(clean)

        except:
            pass

    return urls


# --------------------------------------------------
# Main Reusable Function
# --------------------------------------------------

def run_crawler(website):

    print("\nDiscovering sitemaps...")

    sitemaps = discover_sitemaps(website)

    all_urls = []

    for sitemap in sitemaps:

        print("Found Sitemap:", sitemap)

        all_urls.extend(
            parse_sitemap(sitemap)
        )

    all_urls = list(set(all_urls))

    if not all_urls:

        print(
            "No sitemap found. Using fallback crawler."
        )

        all_urls = crawl_links(website)

    print(
        "\nURLs discovered:",
        len(all_urls)
    )

    results = []

    for i, url in enumerate(
        all_urls[:MAX_PAGES]
    ):

        print(
            f"[{i+1}/{min(len(all_urls), MAX_PAGES)}] {url}"
        )

        page = extract_page(url)

        if page:
            results.append(page)

    with open(
        "all_pages.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    with open(
        "all_pages.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "url",
            "page_type",
            "title",
            "meta_description"
        ])

        for row in results:

            writer.writerow([
                row["url"],
                row["page_type"],
                row["title"],
                row["meta_description"]
            ])

    return {
        "pages_found": len(results),
        "json_file": "all_pages.json",
        "csv_file": "all_pages.csv"
    }


# --------------------------------------------------
# Standalone Mode
# --------------------------------------------------

if __name__ == "__main__":

    website = input(
        "Website URL: "
    ).strip()

    result = run_crawler(website)

    print("\nDone.")
    print(
        "Pages saved:",
        result["pages_found"]
    )