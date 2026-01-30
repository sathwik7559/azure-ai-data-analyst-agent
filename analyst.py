import os
import json
from openai import AzureOpenAI
from prompts import SYSTEM_PROMPT

def _get_client() -> AzureOpenAI:
    # Must be set in local .env and in Azure Container Apps env vars
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    if not api_key or not endpoint or not api_version:
        raise RuntimeError(
            "Missing Azure OpenAI env vars. Required: "
            "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION"
        )

    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )

def _extract_json(text: str) -> dict:
    """
    The model should return strict JSON, but if it wraps text, extract the first JSON object.
    """
    text = text.strip()

    # Already pure JSON
    if text.startswith("{") and text.endswith("}"):
        return json.loads(text)

    # Extract first {...}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end+1])

    raise ValueError("Model did not return valid JSON.")

def generate_analysis_code(schema: dict, df_head: str, question: str) -> dict:
    """
    Returns dict: {"chart_type": "...", "code": "..."}
    """
    client = _get_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise RuntimeError("Missing AZURE_OPENAI_DEPLOYMENT env var (your model deployment name).")

    user_prompt = f"""
DataFrame schema (column -> dtype):
{json.dumps(schema, indent=2)}

DataFrame preview (top rows):
{df_head}

User question:
{question}

Return STRICT JSON ONLY:
{{
  "chart_type": "bar|line|pie|none",
  "code": "..."
}}
"""

    # NOTE:
    # Some Azure models reject temperature=0. Keep defaults unless you know it supports.
    resp = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = resp.choices[0].message.content or ""
    data = _extract_json(content)

    # Hard validation
    chart_type = data.get("chart_type", "none")
    code = data.get("code", "")

    if chart_type not in {"bar", "line", "pie", "none"}:
        chart_type = "none"

    if not isinstance(code, str) or not code.strip():
        raise ValueError("Model returned empty code.")

    return {"chart_type": chart_type, "code": code}