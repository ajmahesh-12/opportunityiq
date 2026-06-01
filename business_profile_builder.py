import json
import re

# -----------------------------------------
# CONFIG
# -----------------------------------------

MAX_TEXT_PER_PAGE = 5000

# -----------------------------------------
# HELPERS
# -----------------------------------------

def truncate_text(text, limit=MAX_TEXT_PER_PAGE):
    if not text:
        return ""
    return text[:limit]

# -----------------------------------------
# LOAD CRAWLED DATA
# -----------------------------------------

with open("all_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

# -----------------------------------------
# PAGE BUCKETS
# -----------------------------------------

homepage = None
about_pages = []
contact_pages = []
service_pages = []
product_pages = []
location_pages = []
faq_pages = []

# -----------------------------------------
# CLASSIFY IMPORTANT PAGES
# -----------------------------------------

for page in pages:

    url = page.get("url", "").lower()
    page_type = page.get("page_type", "other")

    if homepage is None:
        homepage = page

    if page_type == "about":
        about_pages.append(page)

    elif page_type == "contact":
        contact_pages.append(page)

    elif page_type == "service":
        service_pages.append(page)

    elif page_type == "product":
        product_pages.append(page)

    elif page_type == "location":
        location_pages.append(page)

    elif page_type == "faq":
        faq_pages.append(page)

# -----------------------------------------
# BUILD AI INPUT PACKAGE
# -----------------------------------------

business_input = {
    "homepage": {},
    "about_pages": [],
    "contact_pages": [],
    "service_pages": [],
    "product_pages": [],
    "location_pages": [],
    "faq_pages": []
}

# -----------------------------------------
# HOMEPAGE
# -----------------------------------------

if homepage:

    business_input["homepage"] = {
        "url": homepage.get("url"),
        "title": homepage.get("title"),
        "headings": homepage.get("headings", []),
        "text": truncate_text(homepage.get("text", ""))
    }

# -----------------------------------------
# FUNCTION TO SIMPLIFY PAGES
# -----------------------------------------

def simplify_page(page):

    return {
        "url": page.get("url"),
        "title": page.get("title"),
        "headings": page.get("headings", []),
        "text": truncate_text(page.get("text", ""))
    }

# -----------------------------------------
# ADD IMPORTANT PAGES
# -----------------------------------------

for page in about_pages[:5]:
    business_input["about_pages"].append(
        simplify_page(page)
    )

for page in contact_pages[:5]:
    business_input["contact_pages"].append(
        simplify_page(page)
    )

for page in service_pages[:20]:
    business_input["service_pages"].append(
        simplify_page(page)
    )

for page in product_pages[:20]:
    business_input["product_pages"].append(
        simplify_page(page)
    )

for page in location_pages[:20]:
    business_input["location_pages"].append(
        simplify_page(page)
    )

for page in faq_pages[:10]:
    business_input["faq_pages"].append(
        simplify_page(page)
    )

# -----------------------------------------
# SAVE OUTPUT
# -----------------------------------------

with open(
    "business_input.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        business_input,
        f,
        indent=2,
        ensure_ascii=False
    )

# -----------------------------------------
# STATS
# -----------------------------------------

print("\nBusiness Input Package Created\n")

print("About Pages:", len(about_pages))
print("Contact Pages:", len(contact_pages))
print("Service Pages:", len(service_pages))
print("Product Pages:", len(product_pages))
print("Location Pages:", len(location_pages))
print("FAQ Pages:", len(faq_pages))

print("\nSaved:")
print("business_input.json")