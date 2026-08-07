from pathlib import Path

from services.llm_client import client


SCHEMA_PATH = (
    Path(__file__).parent.parent
    / "prompts"
    / "schema.txt"
)


SCHEMA = SCHEMA_PATH.read_text(
    encoding="utf-8"
)



def clean_sql(sql):

    sql = sql.replace(
        "```sql",
        ""
    )

    sql = sql.replace(
        "```",
        ""
    )

    return sql.strip()



def generate_sql(
        question: str,
        context=None
):


    prompt = f"""
你是一名SQL生成助手。

数据库结构：

{SCHEMA}


用户问题：

{question}


上下文：

{context}


要求：

1. 只能使用Schema存在的表和字段

2. 只能生成SELECT语句

3. 如果存在实体信息：

item:
使用item_name查询

brand:
使用brand查询


4. 不允许商品名称查询品牌字段

5. 如果无法查询，返回：
NO_AVAILABLE_FIELD

6. 只返回SQL，不要解释

"""


    response = client.chat.completions.create(

        model="deepseek-chat",

        temperature=0,

        messages=[

            {
                "role":"system",
                "content":
                "你只输出SQL"
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )



    sql = response.choices[0].message.content


    sql = clean_sql(sql)



    return sql