from decimal import Decimal

from services.planner_service import planner
from services.sql_generator import generate_sql
from services.deepseek_service import chat
from services.vector_search import search
from services.chart_service import generate_chart
from tools.mysql_tool import execute_query


# =========================
# 简单上下文记忆
# =========================

memory = {
    "last_result": None,
    "last_entity": None
}


def decimal_to_float(rows):

    for row in rows:
        for k, v in row.items():
            if isinstance(v, Decimal):
                row[k] = float(v)

    return rows



def resolve_context(message):

    entity = memory.get("last_entity")

    if not entity:
        return message


    words = [
        "它",
        "这个商品",
        "这个",
        "那个"
    ]

    for word in words:

        if word in message:
            message = message.replace(
                word,
                entity
            )

    return message



def save_context(data):

    if not data:
        return


    if isinstance(data, list):

        first = data[0]


        # 商品
        if "item_name" in first:
            memory["last_entity"] = first["item_name"]


        # 品牌
        elif "brand" in first:
            memory["last_entity"] = first["brand"]



    memory["last_result"] = data



def run_agent(message):


    # =========================
    # 上下文解析
    # =========================

    original_message = message

    message = resolve_context(message)


    print("================")
    print("用户:", original_message)
    print("解析:", message)
    print("================")



    intent = planner(message).get(
        "intent",
        "chat"
    )



    if intent in ("sql", "chart"):


        sql = generate_sql(message)


        data = decimal_to_float(
            execute_query(sql)
        )


        # 保存上下文
        save_context(data)



        if intent == "chart":

            return {
                "answer": "图表生成完成",
                "chart": generate_chart(
                    data,
                    message
                )
            }



        return {
            "answer": chat(
                f"""
数据库结果：
{data}

用户问题：
{message}

根据数据库结果回答，不要编造数据。
"""
            ),
            "chart": None
        }



    if intent == "rag":


        context = "\n".join(
            search(message)
        )


        return {
            "answer": chat(
                f"""
企业知识：
{context}

用户问题：
{message}

请根据知识回答。
"""
            ),
            "chart": None
        }



    return {
        "answer": chat(message),
        "chart": None
    }