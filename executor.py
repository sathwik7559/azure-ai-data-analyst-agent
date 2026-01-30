import pandas as pd
import traceback
import re

_BLOCKED_PATTERNS = [
    r"\bimport\b",
    r"\bos\.",
    r"\bsys\.",
    r"\bsubprocess\b",
    r"\bsocket\b",
    r"\brequests\b",
    r"\burllib\b",
    r"\bopen\(",
    r"\beval\(",
    r"\bexec\(",
    r"__",
    r"\bpd\.read_",
    r"\bto_csv\b",
    r"\bto_excel\b",
]

def _is_code_safe(code: str) -> (bool, str):
    for pat in _BLOCKED_PATTERNS:
        if re.search(pat, code):
            return False, f"Blocked unsafe pattern detected: {pat}"
    return True, ""

def execute_code(code: str, df: pd.DataFrame):
    ok, reason = _is_code_safe(code)
    if not ok:
        return {"type": "error", "value": reason}

    local_vars = {"df": df}

    try:
        # No globals, minimal locals
        exec(code, {}, local_vars)

        if "final_answer" not in local_vars:
            return {"type": "error", "value": "No variable named 'final_answer' was produced."}

        result = local_vars["final_answer"]

        if isinstance(result, pd.DataFrame):
            return {"type": "dataframe", "value": result}
        if isinstance(result, pd.Series):
            return {"type": "series", "value": result}
        if isinstance(result, (int, float, str)):
            return {"type": "scalar", "value": result}

        return {"type": "error", "value": f"Unsupported result type: {type(result)}"}

    except Exception:
        return {"type": "error", "value": traceback.format_exc()}

def summarize_result(result, max_rows: int = 20) -> str:
    """
    Converts result to a compact text form for the explainer LLM.
    """
    try:
        if isinstance(result, pd.DataFrame):
            return result.head(max_rows).to_string(index=False)
        if isinstance(result, pd.Series):
            return result.head(max_rows).to_string()
        return str(result)
    except Exception:
        return str(result)