from pathlib import Path

from services.llm_client import client

# 加载数据库 Schema
SCHEMA_PATH = Path(__file__).parent.parent / "prompts" / "schema.txt"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = f.read()


def generate_sql(question: str):
    prompt = f"""
你是一名SQL生成助手。

数据库结构：
{SCHEMA}

用户问题：
{question}

要求：
- 只返回SQL
- 只能使用Schema中的表和字段
- 只能生成SELECT语句
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你只输出SQL。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()