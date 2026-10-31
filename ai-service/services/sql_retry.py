from services.sql_generator import generate_sql


def retry_sql(question, error, context, trace=None):

    """把错误原文回传给模型，让它重写一次。

    只带原问题和错误，不带历史，控制输入长度。
    """

    prompt = f"""问题：{question}
上次的 SQL 执行失败：{error}
上下文：{context or "无"}

请改正后只输出一条 SELECT，查不了就返回 NO_AVAILABLE_FIELD。
"""

    return generate_sql(prompt, context=context, trace=trace)
