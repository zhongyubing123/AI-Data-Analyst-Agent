import re
from decimal import Decimal

from services.planner_service import planner
from services.sql_generator import generate_sql
from services.deepseek_service import chat
from services.vector_search import search
from services.chart_service import generate_chart
from tools.mysql_tool import execute_query

from services.memory_service import (
    resolve_context,
    save_context,
    get_context
)


def extract_table(sql):

    match = re.search(
        r"from\s+(\w+)",
        sql,
        re.I
    )

    if match:
        return match.group(1)

    return None



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



    planner_result = planner(message)


    print("================")
    print("Planner结果:", planner_result)
    print("================")


    intent = planner_result.get(
        "intent",
        "chat"
    )


    print("最终Intent:", intent)



    # =========================
    # SQL / Chart
    # =========================

    if intent in ("sql", "chart"):


        sql = generate_sql(
            message,
            context=get_context()
        )
#         sql = sql.replace(
#     "buy_count",
#     "sales_amount"
# )


        print("生成SQL:", sql)



        # Schema不存在字段

        if sql == "NO_AVAILABLE_FIELD":

            return {
                "answer": chat(
                    f"""
用户问题：
{message}

当前数据库Schema中不存在相关字段。

请向用户解释：
1. 当前无法查询该信息
2. 说明数据库支持哪些分析方向
3. 不要编造数据
"""
                ),
                "chart": None
            }



        # =========================
        # SQL执行
        # =========================

        try:

            data = decimal_to_float(
                execute_query(sql)
            )


        except Exception as e:


            print("第一次SQL失败:", e)


            from services.sql_retry import retry_sql


            fixed_sql = retry_sql(
                message,
                str(e),
                get_context()
            )


            print("修复SQL:", fixed_sql)


            try:

                data = decimal_to_float(
                    execute_query(fixed_sql)
                )

                sql = fixed_sql


            except Exception as retry_error:


                print(
                    "SQL修复失败:",
                    retry_error
                )


                return {
                    "answer": f"SQL执行失败: {retry_error}",
                    "chart": None
                }




        print("SQL结果:", data)


        # 保存上下文

        save_context(
            data=data,
            intent=intent,
            sql=sql,
            table=extract_table(sql)
        )



        # =========================
        # 图表
        # =========================

        if intent == "chart":

            return {

                "answer": "图表生成完成",

                "chart": generate_chart(
                    data,
                    message
                )
            }




        # =========================
        # SQL结果回答
        # =========================

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




    # =========================
    # RAG
    # =========================

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




    # =========================
    # 普通聊天
    # =========================

    return {

        "answer": chat(message),

        "chart": None
    }