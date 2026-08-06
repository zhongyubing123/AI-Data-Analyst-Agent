from pathlib import Path

from services.llm_client import client

# 加载数据库 Schema
SCHEMA_PATH = Path(__file__).parent.parent / "prompts" / "schema.txt"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = f.read()


def generate_sql(question: str, context=None):
    prompt = f"""
你是一名SQL生成助手。

数据库结构：
{SCHEMA}

用户问题：
{question}

上下文信息：
{context}

规则：
1. 只能使用Schema中的表和字段
2. 只能生成SELECT语句
3. 如果上下文中存在实体信息：
   - entity_type=item 时，
     商品名称必须使用 item_name 查询
   - entity_type=brand 时，
     品牌名称必须使用 brand 查询
4. 不允许把商品名称当成品牌查询
5. 只返回SQL，不要解释
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

    sql = response.choices[0].message.content.strip()

    if sql == "NO_AVAILABLE_FIELD":
          return sql

    return sql