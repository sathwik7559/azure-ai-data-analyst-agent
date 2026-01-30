import pandas as pd

def summarize_result(result):
    """
    Converts raw pandas / scalar outputs into a compact text summary
    that the LLM can explain in natural language.
    """

    # Scalar
    if isinstance(result, (int, float, str)):
        return str(result)

    # Pandas Series
    if isinstance(result, pd.Series):
        summary_lines = []
        for idx, val in result.items():
            summary_lines.append(f"{idx}: {round(val, 2)}")
        return "\n".join(summary_lines)

    # Pandas DataFrame
    if isinstance(result, pd.DataFrame):
        return result.head(10).to_string()

    return "No summarizable result"