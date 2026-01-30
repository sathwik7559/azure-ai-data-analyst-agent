import os
from openai import AzureOpenAI
from prompts import EXPLAIN_PROMPT

def _get_client() -> AzureOpenAI:
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

def explain_result(question: str, result_summary: str) -> str:
    client = _get_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise RuntimeError("Missing AZURE_OPENAI_DEPLOYMENT env var.")

    prompt = f"""
User question:
{question}

Result summary:
{result_summary}
"""

    resp = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": EXPLAIN_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    return (resp.choices[0].message.content or "").strip()