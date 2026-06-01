import streamlit as st
import json

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

            # ----------------------------------
            # Run Crawler
            # ----------------------------------

            with st.spinner(
                "Crawling website..."
            ):

                crawl_result = run_crawler(
                    website
                )

            # ----------------------------------
            # Build Business Profile
            # ----------------------------------

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

            # ----------------------------------
            # Metrics
            # ----------------------------------

            st.subheader(
                "Analysis Summary"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Pages Crawled",
                    crawl_result["pages_found"]
                )

            with col2:

                st.metric(
                    "Service Pages",
                    profile_result["service_pages"]
                )

            with col3:

                st.metric(
                    "Product Pages",
                    profile_result["product_pages"]
                )

            st.divider()

            # ----------------------------------
            # Download Files
            # ----------------------------------

            st.subheader(
                "Generated Files"
            )

            try:

                with open(
                    "all_pages.json",
                    "r",
                    encoding="utf-8"
                ) as f:

                    all_pages_data = f.read()

                st.download_button(
                    label="Download all_pages.json",
                    data=all_pages_data,
                    file_name="all_pages.json",
                    mime="application/json"
                )

            except:
                pass

            try:

                with open(
                    "business_input.json",
                    "r",
                    encoding="utf-8"
                ) as f:

                    business_input_data = f.read()

                st.download_button(
                    label="Download business_input.json",
                    data=business_input_data,
                    file_name="business_input.json",
                    mime="application/json"
                )

            except:
                pass

            st.divider()

            # ----------------------------------
            # Preview Business Profile
            # ----------------------------------

            st.subheader(
                "Business Profile Preview"
            )

            with open(
                "business_input.json",
                "r",
                encoding="utf-8"
            ) as f:

                business_input = json.load(f)

            homepage = business_input.get(
                "homepage",
                {}
            )

            st.write(
                "### Homepage"
            )

            st.json(homepage)

            services = business_input.get(
                "service_pages",
                []
            )

            if services:

                st.write(
                    "### Sample Services"
                )

                for service in services[:5]:

                    st.write(
                        f"• {service.get('title','No Title')}"
                    )

            products = business_input.get(
                "product_pages",
                []
            )

            if products:

                st.write(
                    "### Sample Products"
                )

                for product in products[:5]:

                    st.write(
                        f"• {product.get('title','No Title')}"
                    )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )