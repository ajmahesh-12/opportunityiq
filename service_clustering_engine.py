import json
import re
from collections import defaultdict

# -------------------------------------
# COMMON WORD REPLACEMENTS
# -------------------------------------

REPLACEMENTS = {

    "ba": "business analysis",

    "analyst": "analysis",

    "training program": "training",

    "certification program": "certification",

    "course": "training",

    "courses": "training",

    "bootcamp": "training",

    "program": "",

    "professional": "",

    "certified": "",

    "level 1": "",

    "level 2": ""
}

# -------------------------------------
# NORMALIZE SERVICE
# -------------------------------------

def normalize_service(service):

    service = service.lower()

    service = service.replace("&", "and")

    for old, new in REPLACEMENTS.items():

        service = service.replace(old, new)

    service = re.sub(
        r"[^a-z0-9 ]",
        " ",
        service
    )

    service = re.sub(
        r"\s+",
        " ",
        service
    )

    return service.strip()

# -------------------------------------
# CREATE CLUSTER KEY
# -------------------------------------

def create_cluster_key(service):

    words = normalize_service(
        service
    ).split()

    words = sorted(set(words))

    return " ".join(words)

# -------------------------------------
# BUILD CLUSTERS
# -------------------------------------

def build_service_clusters():

    with open(
        "service_catalog.json",
        "r",
        encoding="utf-8"
    ) as f:

        catalog = json.load(f)

    clusters = defaultdict(list)

    for item in catalog["services"]:

        service = item["service"]

        mentions = item["mentions"]

        key = create_cluster_key(
            service
        )

        clusters[key].append({

            "service": service,

            "mentions": mentions
        })

    results = []

    for cluster_key, services in clusters.items():

        total_mentions = sum(

            s["mentions"]

            for s in services
        )

        primary_name = max(

            services,

            key=lambda x: x["mentions"]

        )["service"]

        results.append({

            "cluster_name":
                primary_name,

            "cluster_score":
                total_mentions,

            "service_count":
                len(services),

            "services":
                services
        })

    results = sorted(

        results,

        key=lambda x: x["cluster_score"],

        reverse=True
    )

    output = {

        "total_clusters":
            len(results),

        "clusters":
            results
    }

    with open(

        "service_clusters.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            output,

            f,

            indent=2,

            ensure_ascii=False

        )

    return output

# -------------------------------------
# STANDALONE
# -------------------------------------

if __name__ == "__main__":

    clusters = build_service_clusters()

    print(
        "\nService Clusters Created"
    )

    print(
        "Clusters:",
        clusters["total_clusters"]
    )

    print(
        "\nTop Clusters:\n"
    )

    for cluster in clusters[
        "clusters"
    ][:10]:

        print(
            f"{cluster['cluster_name']}"
        )

        print(
            f"Score: {cluster['cluster_score']}"
        )

        print(
            f"Variants: {cluster['service_count']}"
        )

        print()