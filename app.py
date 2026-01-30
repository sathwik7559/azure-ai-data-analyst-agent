import streamlit as st
import pandas as pd

from analyst import generate_analysis_code
from executor import execute_code, summarize_result
from explainer import explain_result


# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="AI Data Analyst Agent",
    layout="wide"
)

st.title("🧠 AI Data Analyst Agent")
st.caption("Ask questions in plain English. The agent analyzes your data, builds charts, and explains insights.")


# ----------------------------
# File upload
# ----------------------------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.subheader("📄 Data Preview")
st.dataframe(df.head())


# ----------------------------
# Question input
# ----------------------------
st.subheader("❓ Ask a question about the data")
question = st.text_input(
    "Example: revenue share by category, top 5 products by sales, total revenue",
    placeholder="Type your question here..."
)


# ----------------------------
# Analyze button
# ----------------------------
if st.button("Analyze") and question:

    with st.spinner("Analyzing data using AI agent..."):
        # Schema info for LLM
        schema = {
            col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)
        }

        df_head = df.head().to_string()

        # 1️⃣ Generate analysis code
        agent_output = generate_analysis_code(
            schema=schema,
            df_head=df_head,
            question=question
        )

        code = agent_output["code"]
        chart_type = agent_output.get("chart_type")

        # 2️⃣ Execute generated code
        result_obj = execute_code(code, df)

    # ----------------------------
    # Show generated code
    # ----------------------------
    st.subheader("🧾 Generated Analysis Code")
    st.code(code, language="python")

    # ----------------------------
    # Handle execution result
    # ----------------------------
    st.subheader("📊 Result")

    if result_obj["type"] == "error":
        st.error(result_obj["value"])
        st.stop()

    result = result_obj["value"]

    # Scalar
    if isinstance(result, (int, float, str)):
        st.success(result)

    # Series
    elif isinstance(result, pd.Series):
        st.write(result)

        if chart_type == "line":
            st.line_chart(result)

        elif chart_type == "pie":
            fig = result.plot.pie(autopct="%1.1f%%").figure
            st.pyplot(fig)

        elif chart_type == "bar":
            st.bar_chart(result)

    # DataFrame
    elif isinstance(result, pd.DataFrame):
        st.dataframe(result)

        if chart_type == "line" and result.shape[1] >= 2:
            st.line_chart(result.set_index(result.columns[0]))

        elif chart_type == "bar" and result.shape[1] >= 2:
            st.bar_chart(result.set_index(result.columns[0]))

    else:
        st.warning("Result returned but could not be visualized.")


    # ----------------------------
    # Explanation (🔥 FIXED PART)
    # ----------------------------
    st.subheader("📝 Explanation")

    result_summary = summarize_result(result)
    explanation = explain_result(question, result_summary)

    st.write(explanation)