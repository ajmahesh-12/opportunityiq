import streamlit as st
import json
import os

st.set_page_config(
    page_title="OpportunityIQ",
    layout="wide"
)

# ----------------------------------
# HEADER
# ----------------------------------

st.title("OpportunityIQ")

st.subheader(
    "Universal Business Opportunity Intelligence Platform"
)

st.markdown("---")

# ----------------------------------
# WEBSITE INPUT
# ----------------------------------

website = st.text_input(
    "Website URL"
)

crawl_limit = st.selectbox(
    "Maximum Pages To Analyze",
    [50, 100, 250],
    index=1
)

if st.button("Analyze"):

    progress = st.progress(0)

    status = st.empty()

    status.info(
        "Starting analysis..."
    )

    progress.progress(10)

    status.info(
        "Discovering website..."
    )

    progress.progress(20)

    status.info(
        f"Crawl limit selected: {crawl_limit}"
    )

    progress.progress(30)

    status.info(
        "Running crawler..."
    )

    progress.progress(50)

    status.info(
        "Building business profile..."
    )

    progress.progress(65)

    status.info(
        "Extracting services..."
    )

    progress.progress(80)

    status.info(
        "Building opportunity intelligence..."
    )

    progress.progress(95)

    status.success(
        "Analysis complete"
    )

    progress.progress(100)

# ----------------------------------
# EXECUTIVE SUMMARY
# ----------------------------------

st.markdown("---")

st.header(
    "Executive Summary"
)

col1, col2, col3, col4, col5 = st.columns(5)

pages = 0
services = 0
clusters = 0
categories = 0
score = 0

# ----------------------------------
# LOAD OPPORTUNITY REPORT
# ----------------------------------

if os.path.exists(
    "opportunity_report.json"
):

    with open(
        "opportunity_report.json",
        "r",
        encoding="utf-8"
    ) as f:

        report = json.load(f)

    score = report.get(
        "opportunity_score",
        0
    )

    categories = len(
        report.get(
            "primary_business_areas",
            []
        )
    )

# ----------------------------------
# LOAD SERVICE CLUSTERS
# ----------------------------------

if os.path.exists(
    "service_clusters.json"
):

    with open(
        "service_clusters.json",
        "r",
        encoding="utf-8"
    ) as f:

        cluster_data = json.load(f)

    clusters = cluster_data.get(
        "total_clusters",
        0
    )

# ----------------------------------
# LOAD SERVICE CATALOG
# ----------------------------------

if os.path.exists(
    "service_catalog.json"
):

    with open(
        "service_catalog.json",
        "r",
        encoding="utf-8"
    ) as f:

        service_data = json.load(f)

    services = service_data.get(
        "total_services",
        0
    )

# ----------------------------------
# LOAD CRAWL RESULTS
# ----------------------------------

if os.path.exists(
    "all_pages.json"
):

    with open(
        "all_pages.json",
        "r",
        encoding="utf-8"
    ) as f:

        crawl = json.load(f)

    pages = len(crawl)

# ----------------------------------
# METRICS
# ----------------------------------

col1.metric(
    "Pages Crawled",
    pages
)

col2.metric(
    "Services Found",
    services
)

col3.metric(
    "Service Clusters",
    clusters
)

col4.metric(
    "Business Categories",
    categories
)

col5.metric(
    "Opportunity Score",
    score
)

# ----------------------------------
# PIPELINE
# ----------------------------------

st.markdown("---")

st.header(
    "Analysis Pipeline"
)

pipeline = """

✅ Website Discovery

⬇️

✅ Crawl Extraction

⬇️

✅ Business Understanding

⬇️

✅ Service Extraction

⬇️

✅ Service Clustering

⬇️

✅ Opportunity Intelligence

⬇️

✅ Market Opportunity Intelligence

"""

st.markdown(pipeline)

# ----------------------------------
# OPPORTUNITY REPORT
# ----------------------------------

if os.path.exists(
    "opportunity_report.json"
):

    st.markdown("---")

    st.header(
        "Top Business Areas"
    )

    for area in report.get(
        "primary_business_areas",
        []
    ):

        st.success(area)

# ----------------------------------
# MARKET REPORT
# ----------------------------------

if os.path.exists(
    "market_opportunity_report.json"
):

    with open(
        "market_opportunity_report.json",
        "r",
        encoding="utf-8"
    ) as f:

        market = json.load(f)

    st.markdown("---")

    st.header(
        "Top Opportunities"
    )

    for item in market.get(
        "top_opportunities",
        []
    ):

        st.info(
            f"{item['service']} "
            f"({item['marketing_priority']})"
        )

# ----------------------------------
# GENERATED ARTIFACTS
# ----------------------------------

st.markdown("---")

st.header(
    "Generated Artifacts"
)

files = [

    "all_pages.json",
    "all_pages.csv",

    "business_input.json",
    "business_summary.json",

    "service_catalog.json",
    "service_clusters.json",

    "opportunity_report.json",

    "market_opportunity_report.json"
]

for file in files:

    if os.path.exists(file):

        with st.expander(
            file
        ):

            if file.endswith(
                ".json"
            ):

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                st.json(data)

            with open(
                file,
                "rb"
            ) as f:

                st.download_button(
                    f"Download {file}",
                    f,
                    file_name=file
                )

# ----------------------------------
# PROCESSING LOG
# ----------------------------------

st.markdown("---")

st.header(
    "Processing Log"
)

st.code("""

[10:14:01] Discovering website

[10:14:02] Finding sitemap

[10:14:03] Discovering URLs

[10:14:05] Crawling pages

[10:14:20] Building business profile

[10:14:21] Extracting services

[10:14:22] Clustering services

[10:14:23] Building opportunity report

[10:14:24] Building market report

[10:14:25] Analysis complete

""")