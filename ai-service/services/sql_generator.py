from pathlib import Path

from services.llm_call import chat_completion


SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "schema.txt"
)

SCHEMA = SCHEMA_PATH.read_text(encoding="utf-8")

SQL_SYSTEM = "你只输出SQL，不要解释。"


def clean_sql(sql):

    sql = sql.replace("```sql", "").replace("```", "")

    return sql.strip()


def build_prompt(question, context=None):

    # schema 放最前面且保持不变，命中上下文缓存
    return f"""{SCHEMA}

问题：{question}
上下文：{context or "无"}

要求：只写一条 SELECT，字段必须来自上面的表，查不了就返回 NO_AVAILABLE_FIELD。
"""


def generate_sql(question: str, context=None, trace=None):

    content, _ = chat_completion(
        [
            {"role": "system", "content": SQL_SYSTEM},
            {"role": "user", "content": build_prompt(question, context)}
        ],
        trace=trace,
        temperature=0,
        max_tokens=200
    )

    return clean_sql(content)
