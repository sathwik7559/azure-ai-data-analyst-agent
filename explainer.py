from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def explain_result(question, result_summary):
    prompt = f"""
You are a data analyst.

User question:
{question}

Analysis result:
{result_summary}

Explain the result in clear, business-friendly natural language.
Avoid technical jargon.
Highlight key insights and implications.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You explain data insights clearly."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()