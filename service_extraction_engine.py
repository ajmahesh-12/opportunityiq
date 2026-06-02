import json
import re
from collections import Counter

# -------------------------------------
# CLEAN TITLE
# -------------------------------------

def clean_title(title):

    if not title:
        return ""

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    title = title.strip()

    return title


# -------------------------------------
# SERVICE FILTER
# -------------------------------------

def looks_like_service(title):

    title = title.lower()

    bad_words = [

        "home",
        "contact",
        "about",
        "privacy",
        "terms",
        "login",
        "register",
        "cart",
        "checkout",
        "blog",
        "faq"
    ]

    for word in bad_words:

        if title == word:
            return False

    return len(title) > 5


# -------------------------------------
# NORMALIZATION
# -------------------------------------

def normalize_service(title):

    title = title.lower()

    title = title.replace(
        "&",
        "and"
    )

    title = re.sub(
        r"[^a-z0-9 ]",
        "",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


# -------------------------------------
# BUILD SERVICE CATALOG
# -------------------------------------

def build_service_catalog():

    with open(
        "all_pages.json",
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)

    raw_services = []

    for page in pages:

        title = clean_title(
            page.get(
                "title",
                ""
            )
        )

        page_type = page.get(
            "page_type",
            ""
        )

        if page_type in [

            "service",
            "product"

        ]:

            if looks_like_service(
                title
            ):

                raw_services.append(
                    title
                )

    normalized = []

    for service in raw_services:

        normalized.append(

            normalize_service(
                service
            )
        )

    counts = Counter(
        normalized
    )

    catalog = []

    for service, count in counts.items():

        catalog.append({

            "service": service,

            "mentions": count

        })

    catalog = sorted(

        catalog,

        key=lambda x: x["mentions"],

        reverse=True

    )

    result = {

        "total_services":

            len(catalog),

        "services":

            catalog
    }

    with open(

        "service_catalog.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            result,

            f,

            indent=2,

            ensure_ascii=False

        )

    return result


# -------------------------------------
# STANDALONE
# -------------------------------------

if __name__ == "__main__":

    catalog = build_service_catalog()

    print(
        "\nService Catalog Created"
    )

    print(
        "Services Found:",
        catalog["total_services"]
    )

    print("\nTop Services:\n")

    for item in catalog[
        "services"
    ][:20]:

        print(
            item["service"],
            "(",
            item["mentions"],
            ")"
        )