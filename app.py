%%writefile app.py

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Responsible AI Bias Audit",
    page_icon="⚖️",
    layout="wide"
)

st.title("Responsible AI and Bias Audit of a Chatbot")

st.write(
    "This project checks chatbot responses "
    "for fairness, respectful language, and consistency."
)

if "results" not in st.session_state:
    st.session_state.results = []

menu = st.sidebar.selectbox(
    "Select Menu",
    ["Dashboard", "Bias Audit", "Results", "About"]
)

if menu == "Dashboard":

    st.header("Project Dashboard")

    st.metric(
        "Total Audits",
        len(st.session_state.results)
    )

    st.write("### Project Objectives")

    st.write("1. Identify possible chatbot bias.")
    st.write("2. Compare different chatbot responses.")
    st.write("3. Evaluate fairness and accuracy.")
    st.write("4. Record audit results.")
    st.write("5. Suggest improvements.")

elif menu == "Bias Audit":

    st.header("Chatbot Bias Audit")

    with st.form("audit_form"):

        test_id = st.text_input("Test ID")

        category = st.selectbox(
            "Bias Category",
            ["Gender", "Language", "Accessibility", "Age", "Other"]
        )

        prompt_a = st.text_area("Prompt A")
        response_a = st.text_area("Chatbot Response A")

        prompt_b = st.text_area("Prompt B")
        response_b = st.text_area("Chatbot Response B")

        st.subheader("Audit Evaluation")

        fairness = st.selectbox("Fairness", [0, 1, 2])
        tone = st.selectbox("Respectful Tone", [0, 1, 2])
        relevance = st.selectbox("Relevance", [0, 1, 2])
        consistency = st.selectbox("Consistency", [0, 1, 2])
        accuracy = st.selectbox("Accuracy", [0, 1, 2])

        risk = st.selectbox(
            "Risk Level",
            ["Low", "Medium", "High"]
        )

        notes = st.text_area("Observations")

        submitted = st.form_submit_button("Submit Audit")

    if submitted:

        if not all([
            test_id.strip(),
            prompt_a.strip(),
            response_a.strip(),
            prompt_b.strip(),
            response_b.strip()
        ]):

            st.error("Please complete all required fields.")

        else:

            score = (
                fairness
                + tone
                + relevance
                + consistency
                + accuracy
            )

            record = {
                "Test ID": test_id,
                "Category": category,
                "Prompt A": prompt_a,
                "Response A": response_a,
                "Prompt B": prompt_b,
                "Response B": response_b,
                "Fairness": fairness,
                "Tone": tone,
                "Relevance": relevance,
                "Consistency": consistency,
                "Accuracy": accuracy,
                "Score / 10": score,
                "Risk": risk,
                "Observations": notes,
                "Date": datetime.now().strftime("%Y-%m-%d")
            }

            st.session_state.results.append(record)

            st.success("Audit saved successfully!")

            st.metric("Audit Score", f"{score}/10")

elif menu == "Results":

    st.header("Audit Results")

    if st.session_state.results:

        df = pd.DataFrame(st.session_state.results)

        st.dataframe(df, use_container_width=True)

        st.subheader("Audit Score Chart")

        st.bar_chart(
            df.set_index("Test ID")["Score / 10"]
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Results CSV",
            data=csv,
            file_name="bias_audit_results.csv",
            mime="text/csv"
        )

    else:

        st.info("No audit results available yet.")

elif menu == "About":

    st.header("About This Project")

    st.write("""
    Project Name:
    Responsible AI and Bias Audit of a Chatbot

    Technology:
    Python, Streamlit, Pandas

    Purpose:
    To identify possible differences in chatbot responses.

    Evaluation Criteria:
    - Fairness
    - Respectful Tone
    - Relevance
    - Consistency
    - Accuracy

    Note:
    Results depend on the prompts tested and human evaluation.
    A score does not prove that a chatbot is unbiased.
    """)
