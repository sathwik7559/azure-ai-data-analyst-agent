import pandas as pd

def execute_code(code: str, df: pd.DataFrame):
    local_vars = {"df": df.copy()}

    try:
        exec(code, {}, local_vars)
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

    if "final_answer" not in local_vars:
        return {
            "status": "error",
            "error": "final_answer was not produced by the analysis code"
        }

    result = local_vars["final_answer"]

    # Scalar
    if isinstance(result, (int, float, str)):
        return {
            "status": "ok",
            "type": "scalar",
            "value": result
        }

    # Pandas Series
    if isinstance(result, pd.Series):
        return {
            "status": "ok",
            "type": "series",
            "value": result
        }

    # Pandas DataFrame
    if isinstance(result, pd.DataFrame):
        return {
            "status": "ok",
            "type": "dataframe",
            "value": result
        }

    return {
        "status": "error",
        "error": f"Unsupported return type: {type(result)}"
    }


def summarize_result(result):
    if isinstance(result, (int, float)):
        return f"Value: {result}"

    if isinstance(result, str):
        return result

    if hasattr(result, "head"):
        return result.head().to_string()

    return str(result)