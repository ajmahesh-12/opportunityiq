import streamlit as st

from crawler_v3 import run_crawler
from business_profile_builder_v2 import build_business_profile


st.set_page_config(
    page_title="OpportunityIQ",
    layout="wide"
)

st.title("OpportunityIQ")

st.write(
    "Universal Business Opportunity Intelligence Platform"
)

website = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com"
)

if st.button("Analyze"):

    if not website:

        st.error(
            "Please enter a website URL."
        )

    else:

        try:

            # -----------------------------
            # Crawl Website
            # -----------------------------

            with st.spinner(
                "Crawling website..."
            ):

                crawl_result = run_crawler(
                    website
                )

            # -----------------------------
            # Build Business Profile
            # -----------------------------

            with st.spinner(
                "Building business profile..."
            ):

                profile_result = (
                    build_business_profile()
                )

            st.success(
                "Analysis Complete"
            )

            st.divider()

            # -----------------------------
            # Metrics
            # -----------------------------

            st.subheader(
                "Crawler Results"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Pages Crawled",
                    crawl_result["pages_found"]
                )

            with col2:

                st.metric(
                    "JSON Output",
                    crawl_result["json_file"]
                )

            st.divider()

            # -----------------------------
            # Business Profile
            # -----------------------------

            st.subheader(
                "Business Profile Summary"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Service Pages",
                    profile_result[
                        "service_pages"
                    ]
                )

                st.metric(
                    "About Pages",
                    profile_result[
                        "about_pages"
                    ]
                )

            with c2:

                st.metric(
                    "Product Pages",
                    profile_result[
                        "product_pages"
                    ]
                )

                st.metric(
                    "Contact Pages",
                    profile_result[
                        "contact_pages"
                    ]
                )

            with c3:

                st.metric(
                    "Location Pages",
                    profile_result[
                        "location_pages"
                    ]
                )

                st.metric(
                    "FAQ Pages",
                    profile_result[
                        "faq_pages"
                    ]
                )

            st.divider()

            # -----------------------------
            # Generated Files
            # -----------------------------

            st.subheader(
                "Generated Files"
            )

            st.write(
                "✓ all_pages.json"
            )

            st.write(
                "✓ all_pages.csv"
            )

            st.write(
                "✓ business_input.json"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )