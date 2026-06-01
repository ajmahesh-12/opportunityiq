import json

MAX_TEXT_PER_PAGE = 5000


def truncate_text(text, limit=MAX_TEXT_PER_PAGE):
    if not text:
        return ""
    return text[:limit]


def simplify_page(page):

    return {
        "url": page.get("url"),
        "title": page.get("title"),
        "headings": page.get("headings", []),
        "text": truncate_text(
            page.get("text", "")
        )
    }


def build_business_profile():

    with open(
        "all_pages.json",
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)

    homepage = None

    about_pages = []
    contact_pages = []
    service_pages = []
    product_pages = []
    location_pages = []
    faq_pages = []

    for page in pages:

        page_type = page.get(
            "page_type",
            "other"
        )

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

    business_input = {
        "homepage": {},
        "about_pages": [],
        "contact_pages": [],
        "service_pages": [],
        "product_pages": [],
        "location_pages": [],
        "faq_pages": []
    }

    if homepage:

        business_input["homepage"] = {
            "url": homepage.get("url"),
            "title": homepage.get("title"),
            "headings": homepage.get(
                "headings",
                []
            ),
            "text": truncate_text(
                homepage.get(
                    "text",
                    ""
                )
            )
        }

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

    return {
        "about_pages": len(about_pages),
        "contact_pages": len(contact_pages),
        "service_pages": len(service_pages),
        "product_pages": len(product_pages),
        "location_pages": len(location_pages),
        "faq_pages": len(faq_pages)
    }


if __name__ == "__main__":

    stats = build_business_profile()

    print(stats)