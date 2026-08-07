from services.sql_generator import generate_sql



def retry_sql(
    question,
    error,
    context
):


    retry_question = f"""

用户问题：

{question}


SQL执行失败。


错误：

{error}


请修复SQL。


要求：

1. 保持原查询意图
2. 修复字段错误
3. 返回完整查询结果字段
4. 只输出SQL

"""


    return generate_sql(
        retry_question,
        context=context
    )