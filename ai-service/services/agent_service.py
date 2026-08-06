import re
from decimal import Decimal

from services.planner_service import planner
from services.sql_generator import generate_sql
from services.deepseek_service import chat
from services.vector_search import search
from services.chart_service import generate_chart
from tools.mysql_tool import execute_query

import re


def extract_table(sql):

    match = re.search(
        r"from\s+(\w+)",
        sql,
        re.I
    )

    if match:
        return match.group(1)

    return None


from services.memory_service import (
    resolve_context,
    save_context
)



def decimal_to_float(rows):

    for row in rows:
        for k, v in row.items():
            if isinstance(v, Decimal):
                row[k] = float(v)

    return rows




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
        print("SQL结果:", data)
        print("SQL:", sql)

        # 保存上下文
        save_context(   
            data=data,
            intent=intent,
            sql=sql,
            table=extract_table(sql)
            
    )



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