import streamlit as st

st.title("OpportunityIQ")

website = st.text_input(
    "Enter Website URL"
)

if st.button("Analyze"):

    st.success(
        f"Analyzing {website}"
    )