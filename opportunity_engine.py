import json
from collections import Counter

# -------------------------------------
# OPPORTUNITY CATEGORIES
# -------------------------------------

CATEGORIES = {

    "Artificial Intelligence": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "prompt",
        "gpt"
    ],

    "Cloud": [
        "cloud",
        "aws",
        "azure",
        "gcp"
    ],

    "Healthcare": [
        "healthcare",
        "medical",
        "hospital",
        "payer",
        "provider"
    ],

    "Cybersecurity": [
        "cyber",
        "security",
        "soc",
        "threat"
    ],

    "Business Analysis": [
        "business analysis",
        "business analyst",
        "cbap",
        "analysis"
    ],

    "Project Management": [
        "project",
        "pmp",
        "scrum",
        "agile"
    ],

    "Data": [
        "data",
        "analytics",
        "sql",
        "engineer",
        "warehouse"
    ]
}


# -------------------------------------
# SCORE CATEGORY
# -------------------------------------

def score_categories(summary):

    scores = Counter()

    text_pool = []

    text_pool.extend(
        summary.get("services", [])
    )

    text_pool.extend(
        summary.get("products", [])
    )

    text_pool.extend(
        summary.get("top_keywords", [])
    )

    combined_text = " ".join(
        text_pool
    ).lower()

    for category, keywords in CATEGORIES.items():

        score = 0

        for keyword in keywords:

            score += combined_text.count(
                keyword.lower()
            )

        scores[category] = score

    return scores


# -------------------------------------
# CALCULATE OPPORTUNITY SCORE
# -------------------------------------

def calculate_score(summary, category_scores):

    score = 0

    score += min(
        len(summary.get("services", [])) * 2,
        30
    )

    score += min(
        len(summary.get("products", [])) * 1,
        20
    )

    score += min(
        len(summary.get("top_keywords", [])) // 2,
        20
    )

    score += min(
        sum(category_scores.values()),
        30
    )

    return min(score, 100)


# -------------------------------------
# BUILD REPORT
# -------------------------------------

def build_opportunity_report():

    with open(
        "business_summary.json",
        "r",
        encoding="utf-8"
    ) as f:

        summary = json.load(f)

    category_scores = score_categories(
        summary
    )

    ranked_categories = sorted(
        category_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    opportunity_score = calculate_score(
        summary,
        category_scores
    )

    report = {

        "company_name":
            summary.get(
                "company_name",
                ""
            ),

        "website":
            summary.get(
                "website",
                ""
            ),

        "opportunity_score":
            opportunity_score,

        "primary_business_areas": [

            category

            for category, score

            in ranked_categories

            if score > 0

        ][:5],

        "category_scores": dict(
            ranked_categories
        ),

        "top_services":
            summary.get(
                "services",
                []
            )[:10],

        "top_products":
            summary.get(
                "products",
                []
            )[:10],

        "top_keywords":
            summary.get(
                "top_keywords",
                []
            )[:20]
    }

    with open(
        "opportunity_report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )

    return report


# -------------------------------------
# STANDALONE MODE
# -------------------------------------

if __name__ == "__main__":

    report = build_opportunity_report()

    print(
        "\nOpportunity Report Created"
    )

    print(
        "\nCompany:",
        report["company_name"]
    )

    print(
        "Score:",
        report["opportunity_score"]
    )

    print(
        "Top Areas:"
    )

    for area in report[
        "primary_business_areas"
    ]:

        print("-", area)