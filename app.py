import streamlit as st
import pandas as pd

from analyst import generate_analysis_code
from executor import execute_code, summarize_result
from explainer import explain_result


def infer_chart_type_fallback(question: str, result_obj: dict, suggested: str | None) -> str:
    """
    If the model says 'bar' always, we still apply fallback heuristics
    depending on result shape + question signals.
    """
    q = (question or "").lower()
    suggested = suggested or "none"

    # If model says none, keep none unless we strongly know it's chartable
    if result_obj["type"] == "scalar":
        return "none"

    if result_obj["type"] == "series":
        s = result_obj["value"]

        # Time-ish index -> line
        if pd.api.types.is_datetime64_any_dtype(s.index):
            return "line"

        # "trend", "over time", "daily", "monthly" -> line
        if any(k in q for k in ["trend", "over time", "daily", "weekly", "monthly", "yearly", "by date"]):
            return "line"

        # "share", "percentage", "distribution" and small count -> pie
        if any(k in q for k in ["share", "percentage", "percent", "distribution", "breakdown"]) and len(s) <= 10:
            return "pie"

        # default for series
        return suggested if suggested in {"bar", "line", "pie"} else "bar"

    if result_obj["type"] == "dataframe":
        df = result_obj["value"]
        if df.shape[1] < 2:
            return "none"

        # If first column looks date-like -> line
        first_col = df.columns[0]
        if pd.api.types.is_datetime64_any_dtype(df[first_col]):
            return "line"

        # if question indicates trend/time
        if any(k in q for k in ["trend", "over time", "daily", "weekly", "monthly", "yearly", "by date"]):
            return "line"

        # default
        return suggested if suggested in {"bar", "line"} else "bar"

    return "none"


def render_chart(chart_type: str, result_obj: dict):
    if chart_type == "none":
        return

    if result_obj["type"] == "series":
        s = result_obj["value"]
        if chart_type == "line":
            st.line_chart(s)
        elif chart_type == "bar":
            st.bar_chart(s)
        elif chart_type == "pie":
            fig = s.plot.pie(autopct="%1.1f%%").figure
            st.pyplot(fig)

    elif result_obj["type"] == "dataframe":
        df = result_obj["value"]

        # Expect first column label, second numeric
        if df.shape[1] >= 2:
            plot_df = df.set_index(df.columns[0])
            if chart_type == "line":
                st.line_chart(plot_df)
            elif chart_type == "bar":
                st.bar_chart(plot_df)


# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="AI Data Analyst Agent", layout="wide")
st.title("AI Data Analyst Agent")
st.caption("Upload a CSV, ask a question, get results, charts, and explanation.")


# ----------------------------
# Upload
# ----------------------------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file to start.")
    st.stop()

df = pd.read_csv(uploaded_file)

st.subheader("Data Preview")
st.dataframe(df.head(10), use_container_width=True)


# ----------------------------
# Question
# ----------------------------
st.subheader("Ask a question about the data")
question = st.text_input(
    "Example: top 5 categories by revenue, monthly sales trend, revenue share by category",
    placeholder="Type your question here..."
)

analyze_clicked = st.button("Analyze")


if analyze_clicked and question:
    with st.spinner("Running analysis..."):

        schema = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
        df_head = df.head(8).to_string(index=False)

        # 1) Generate analysis code (LLM)
        agent_output = generate_analysis_code(schema=schema, df_head=df_head, question=question)
        code = agent_output.get("code", "")
        suggested_chart = agent_output.get("chart_type", "none")

        # 2) Execute
        result_obj = execute_code(code, df)

    # Show code
    st.subheader("Generated Analysis Code")
    st.code(code, language="python")

    # Result
    st.subheader("Result")
    if result_obj["type"] == "error":
        st.error(result_obj["value"])
        st.stop()

    if result_obj["type"] == "scalar":
        st.success(result_obj["value"])

    elif result_obj["type"] == "series":
        st.write(result_obj["value"])

    elif result_obj["type"] == "dataframe":
        st.dataframe(result_obj["value"], use_container_width=True)

    # Chart
    final_chart = infer_chart_type_fallback(question, result_obj, suggested_chart)
    st.subheader("Chart")
    render_chart(final_chart, result_obj)

    # Explanation
    st.subheader("Explanation")
    result_summary = summarize_result(result_obj["value"])
    explanation = explain_result(question, result_summary)
    st.write(explanation)