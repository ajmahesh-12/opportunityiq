import streamlit as st
import json
import os

from pipeline import run_pipeline

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="OpportunityIQ",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "OpportunityIQ"
)

st.subheader(
    "Universal Business Opportunity Intelligence Platform"
)

st.markdown(
    """
OpportunityIQ crawls a company website and converts
raw web content into business intelligence,
service intelligence, and market opportunity insights.
"""
)

# --------------------------------------------------
# INPUTS
# --------------------------------------------------

website = st.text_input(
    "Website URL",
    placeholder="https://company.com"
)

crawl_mode = st.selectbox(
    "Analysis Depth",
    [
        "Quick Scan (50 pages)",
        "Standard Scan (100 pages)",
        "Deep Scan (250 pages)"
    ]
)

if crawl_mode.startswith("Quick"):
    max_pages = 50

elif crawl_mode.startswith("Standard"):
    max_pages = 100

else:
    max_pages = 250

st.info(
    f"""
Selected Crawl Limit: {max_pages} pages

OpportunityIQ first discovers all URLs available on
the website.

If more URLs exist than the selected limit,
only the first {max_pages} pages are analyzed.

This keeps analysis time reasonable while
still capturing the majority of business intelligence.

Future enterprise versions can support
thousands of pages.
"""
)

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("Analyze Website"):

    if not website:

        st.error(
            "Enter a website URL."
        )

        st.stop()

    logs = []

    progress = st.progress(0)

    log_area = st.empty()

    # ------------------------------------------
    # LOGGER
    # ------------------------------------------

    def logger(message):

        logs.append(message)

        log_area.text(
            "\n".join(logs[-50:])
        )

    # ------------------------------------------
    # RUN PIPELINE
    # ------------------------------------------

    try:

        progress.progress(5)

        results = run_pipeline(
            website=website,
            max_pages=max_pages,
            logger=logger
        )

        progress.progress(100)

        st.success(
            "Analysis Complete"
        )

    except Exception as e:

        st.error(str(e))
        st.stop()

    # --------------------------------------------------
    # EXECUTIVE DASHBOARD
    # --------------------------------------------------

    st.header(
        "Executive Dashboard"
    )

    crawl = results["crawl"]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "URLs Discovered",
            crawl[
                "total_urls_discovered"
            ]
        )

    with col2:

        st.metric(
            "Pages Crawled",
            crawl[
                "pages_found"
            ]
        )

    with col3:

        coverage = round(
            (
                crawl["pages_found"]
                /
                max(
                    crawl[
                        "total_urls_discovered"
                    ],
                    1
                )
            )
            * 100,
            1
        )

        st.metric(
            "Coverage %",
            coverage
        )

    # --------------------------------------------------
    # OPPORTUNITY REPORT
    # --------------------------------------------------

    if os.path.exists(
        "opportunity_report.json"
    ):

        with open(
            "opportunity_report.json",
            "r",
            encoding="utf-8"
        ) as f:

            opportunity = json.load(f)

        st.header(
            "Opportunity Intelligence"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Opportunity Score",
                opportunity.get(
                    "opportunity_score",
                    0
                )
            )

        with col2:

            st.metric(
                "Business Areas",
                len(
                    opportunity.get(
                        "primary_business_areas",
                        []
                    )
                )
            )

        st.write(
            opportunity
        )

    # --------------------------------------------------
    # MARKET REPORT
    # --------------------------------------------------

    if os.path.exists(
        "market_opportunity_report.json"
    ):

        with open(
            "market_opportunity_report.json",
            "r",
            encoding="utf-8"
        ) as f:

            market = json.load(f)

        st.header(
            "Market Opportunity Report"
        )

        st.json(
            market
        )

    # --------------------------------------------------
    # ARTIFACT HIERARCHY
    # --------------------------------------------------

    st.header(
        "Analysis Artifacts"
    )

    st.markdown(
        """
### Final Intelligence Outputs

- opportunity_report.json
- market_opportunity_report.json

### Business Intelligence Layer

- business_summary.json
- business_input.json

### Service Intelligence Layer

- service_catalog.json
- service_clusters.json

### Crawl Intelligence Layer

- all_pages.json
- all_pages.csv
"""
    )

    # --------------------------------------------------
    # FILE PREVIEW
    # --------------------------------------------------

    artifact_files = [

        "opportunity_report.json",

        "market_opportunity_report.json",

        "business_summary.json",

        "business_input.json",

        "service_catalog.json",

        "service_clusters.json",

        "all_pages.json"
    ]

    for file in artifact_files:

        if os.path.exists(file):

            st.subheader(file)

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            preview = content[:5000]

            st.code(
                preview,
                language="json"
            )

            st.download_button(
                label=f"Download {file}",
                data=content,
                file_name=file
            )

    # --------------------------------------------------
    # RAW LOGS
    # --------------------------------------------------

    st.header(
        "Execution Logs"
    )

    st.text(
        "\n".join(logs)
    )