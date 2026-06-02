import json
from collections import Counter

# --------------------------------------
# OPPORTUNITY SCORING RULES
# --------------------------------------

HIGH_VALUE_KEYWORDS = [

    "ai",
    "cloud",
    "healthcare",
    "security",
    "cyber",
    "automation",
    "analytics",
    "data",
    "software",
    "consulting",
    "training",
    "certification",
    "crm",
    "sales",
    "marketing"
]

# --------------------------------------
# SCORE SERVICES
# --------------------------------------

def score_service(service_name, keywords):

    score = 0

    service_lower = service_name.lower()

    for keyword in keywords:

        if keyword in service_lower:
            score += 10

    return score

# --------------------------------------
# BUILD MARKET OPPORTUNITY REPORT
# --------------------------------------

def build_market_opportunity_report():

    with open(
        "opportunity_report.json",
        "r",
        encoding="utf-8"
    ) as f:

        opportunity = json.load(f)

    services = opportunity.get(
        "top_services",
        []
    )

    keywords = opportunity.get(
        "top_keywords",
        []
    )

    ranked_services = []

    for service in services:

        score = score_service(
            service,
            keywords
        )

        ranked_services.append({

            "service": service,
            "score": score

        })

    ranked_services = sorted(

        ranked_services,

        key=lambda x: x["score"],

        reverse=True

    )

    top_opportunities = []

    for item in ranked_services[:5]:

        service = item["service"]

        score = item["score"]

        if score >= 30:
            priority = "High"

        elif score >= 10:
            priority = "Medium"

        else:
            priority = "Low"

        top_opportunities.append({

            "service": service,

            "opportunity_score": score,

            "marketing_priority": priority

        })

    report = {

        "company_name":
            opportunity.get(
                "company_name",
                ""
            ),

        "overall_opportunity_score":
            opportunity.get(
                "opportunity_score",
                0
            ),

        "top_opportunities":
            top_opportunities,

        "business_areas":
            opportunity.get(
                "primary_business_areas",
                []
            )
    }

    with open(
        "market_opportunity_report.json",
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

# --------------------------------------
# STANDALONE MODE
# --------------------------------------

if __name__ == "__main__":

    report = build_market_opportunity_report()

    print(
        "\nMarket Opportunity Report Created"
    )

    print(
        "\nCompany:",
        report["company_name"]
    )

    print(
        "\nTop Opportunities:"
    )

    for item in report[
        "top_opportunities"
    ]:

        print(
            f"- {item['service']} "
            f"({item['marketing_priority']})"
        )