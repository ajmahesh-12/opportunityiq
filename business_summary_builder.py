import json
import re
from collections import Counter


# -------------------------------------
# STOP WORDS
# -------------------------------------

STOP_WORDS = {
    "the","and","for","with","you","your",
    "our","from","that","this","have",
    "will","are","was","were","been",
    "their","they","them","about","into",
    "more","than","what","when","where",
    "which","who","why","how","can",
    "all","any","each","few","other",
    "some","such","only","own","same",
    "too","very","www","https","http"
}


# -------------------------------------
# EXTRACT KEYWORDS
# -------------------------------------

def extract_keywords(text):

    words = re.findall(
        r"\b[a-zA-Z]{4,20}\b",
        text.lower()
    )

    filtered = [
        w for w in words
        if w not in STOP_WORDS
    ]

    return filtered


# -------------------------------------
# BUILD SUMMARY
# -------------------------------------

def build_business_summary():

    with open(
        "all_pages.json",
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)

    summary = {

        "company_name": "",

        "industry": "",

        "website": "",

        "services": [],

        "products": [],

        "locations": [],

        "contact_pages": [],

        "top_keywords": [],

        "page_counts": {}
    }

    keyword_counter = Counter()

    service_titles = set()
    product_titles = set()
    location_urls = set()
    contact_urls = set()

    for page in pages:

        page_type = page.get(
            "page_type",
            "other"
        )

        title = page.get(
            "title",
            ""
        )

        url = page.get(
            "url",
            ""
        )

        text = page.get(
            "text",
            ""
        )

        if not summary["website"]:
            summary["website"] = url

        if not summary["company_name"]:

            summary["company_name"] = title

        keywords = extract_keywords(
            title + " " + text[:3000]
        )

        keyword_counter.update(
            keywords
        )

        if page_type == "service":

            if title:
                service_titles.add(title)

        if page_type == "product":

            if title:
                product_titles.add(title)

        if page_type == "location":

            location_urls.add(url)

        if page_type == "contact":

            contact_urls.add(url)

    summary["services"] = list(
        service_titles
    )[:50]

    summary["products"] = list(
        product_titles
    )[:50]

    summary["locations"] = list(
        location_urls
    )

    summary["contact_pages"] = list(
        contact_urls
    )

    summary["top_keywords"] = [

        word

        for word, count

        in keyword_counter.most_common(50)
    ]

    summary["page_counts"] = {

        "services": len(
            service_titles
        ),

        "products": len(
            product_titles
        ),

        "locations": len(
            location_urls
        ),

        "contacts": len(
            contact_urls
        )
    }

    with open(
        "business_summary.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False
        )

    return summary


# -------------------------------------
# STANDALONE MODE
# -------------------------------------

if __name__ == "__main__":

    result = build_business_summary()

    print(
        "\nBusiness Summary Created"
    )

    print(
        "Services:",
        len(result["services"])
    )

    print(
        "Products:",
        len(result["products"])
    )

    print(
        "Keywords:",
        len(result["top_keywords"])
    )