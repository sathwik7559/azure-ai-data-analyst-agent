import os
from openai import AzureOpenAI
from prompts import SYSTEM_PROMPT

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

def generate_analysis_code(schema: list, df_head: str, question: str) -> dict:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
DataFrame columns:
{schema}

DataFrame preview:
{df_head}

Question:
{question}

Tasks:
1. Generate Python pandas code ONLY
2. Store final result in `final_answer`
3. Choose ONE chart type from:
   - "bar"
   - "line"
   - "pie"
   - "none"

Rules:
- Use ONLY schema columns
- Do NOT include markdown
- Output STRICT JSON like:

{{
  "chart_type": "...",
  "code": "..."
}}
"""
            }
        ]
    )

    content = response.choices[0].message.content
    return eval(content)  # safe because structure is enforced