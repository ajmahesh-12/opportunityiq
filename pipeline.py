from crawler_v3 import run_crawler

from business_profile_builder_v2 import (
    build_business_profile
)

from business_summary_builder import (
    build_business_summary
)

from service_extraction_engine import (
    build_service_catalog
)

from service_clustering_engine import (
    build_service_clusters
)

from opportunity_engine import (
    build_opportunity_report
)

from market_opportunity_engine import (
    build_market_opportunity_report
)


# --------------------------------------------------
# LOGGER
# --------------------------------------------------

def log(message, logger=None):

    print(message)

    if logger:
        logger(message)


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

def run_pipeline(
    website,
    max_pages=100,
    logger=None
):

    results = {}

    # ------------------------------------------
    # STAGE 1
    # ------------------------------------------

    log(
        "Stage 1/7 : Website Crawl",
        logger
    )

    crawl_result = run_crawler(
        website=website,
        max_pages=max_pages,
        logger=logger
    )

    results["crawl"] = crawl_result

    # ------------------------------------------
    # STAGE 2
    # ------------------------------------------

    log(
        "Stage 2/7 : Business Profile",
        logger
    )

    profile_result = (
        build_business_profile()
    )

    results[
        "business_profile"
    ] = profile_result

    # ------------------------------------------
    # STAGE 3
    # ------------------------------------------

    log(
        "Stage 3/7 : Business Summary",
        logger
    )

    summary_result = (
        build_business_summary()
    )

    results[
        "business_summary"
    ] = summary_result

    # ------------------------------------------
    # STAGE 4
    # ------------------------------------------

    log(
        "Stage 4/7 : Service Extraction",
        logger
    )

    service_result = (
        build_service_catalog()
    )

    results[
        "service_catalog"
    ] = service_result

    # ------------------------------------------
    # STAGE 5
    # ------------------------------------------

    log(
        "Stage 5/7 : Service Clustering",
        logger
    )

    cluster_result = (
        build_service_clusters()
    )

    results[
        "service_clusters"
    ] = cluster_result

    # ------------------------------------------
    # STAGE 6
    # ------------------------------------------

    log(
        "Stage 6/7 : Opportunity Engine",
        logger
    )

    opportunity_result = (
        build_opportunity_report()
    )

    results[
        "opportunity_report"
    ] = opportunity_result

    # ------------------------------------------
    # STAGE 7
    # ------------------------------------------

    log(
        "Stage 7/7 : Market Opportunity Engine",
        logger
    )

    market_result = (
        build_market_opportunity_report()
    )

    results[
        "market_opportunity_report"
    ] = market_result

    log(
        "Pipeline Complete",
        logger
    )

    return results


# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------

if __name__ == "__main__":

    website = input(
        "Website URL: "
    ).strip()

    result = run_pipeline(
        website=website,
        max_pages=100
    )

    print(
        "\nPipeline Complete"
    )

    print(
        "\nPages Crawled:",
        result["crawl"][
            "pages_found"
        ]
    )

    print(
        "URLs Discovered:",
        result["crawl"][
            "total_urls_discovered"
        ]
    )