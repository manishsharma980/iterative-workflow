import streamlit as st
from essay import work

st.title("UPSC Essay Evaluator")

essay = st.text_area("Enter your essay")

if st.button("Evaluate Essay"):

    if essay.strip():

        result = work.invoke({
            "essay": essay,
            "language_feedback": "",
            "analysis_feedback": "",
            "clarity_feedback": "",
            "overall_feedback": "",
            "individual_scores": [],
            "avg_score": 0.0
        })

        st.subheader("Result")

        st.write("Average Score:", result["avg_score"])
        st.write("Language:", result["language_feedback"])
        st.write("Clarity:", result["clarity_feedback"])
        st.write("Analysis:", result["analysis_feedback"])
        st.write("Overall:", result["overall_feedback"])

    else:
        st.warning("Please enter an essay.")