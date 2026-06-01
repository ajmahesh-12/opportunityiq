import json
import re
from collections import Counter

STOPWORDS = {
    "the","and","or","is","a","an","to","of","for",
    "with","on","in","at","by","from","that","this",
    "are","be","as","it","your","you","our","we"
}

def clean_words(text):

    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    return [
        w for w in words
        if w not in STOPWORDS
    ]

def extract_keywords(text, top_n=15):

    words = clean_words(text)

    counts = Counter(words)

    return [
        word
        for word, count
        in counts.most_common(top_n)
    ]

def create_summary(text):

    if not text:
        return ""

    paragraphs = text.split(".")

    if len(paragraphs) == 0:
        return ""

    return ".".join(paragraphs[:3]).strip()

with open(
    "business_input.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

summary = {
    "homepage": {},
    "important_pages": []
}

# Homepage

if data.get("homepage"):

    homepage = data["homepage"]

    text = homepage.get("text","")

    summary["homepage"] = {
        "title": homepage.get("title"),
        "summary": create_summary(text),
        "keywords": extract_keywords(text)
    }

# All page groups

groups = [
    "about_pages",
    "service_pages",
    "product_pages",
    "location_pages",
    "faq_pages"
]

for group in groups:

    for page in data.get(group, []):

        text = page.get("text","")

        summary["important_pages"].append({

            "page_type": group,

            "url": page.get("url"),

            "title": page.get("title"),

            "summary": create_summary(text),

            "keywords": extract_keywords(text)
        })

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

print("Saved business_summary.json")
print("Pages summarized:",
      len(summary["important_pages"]))