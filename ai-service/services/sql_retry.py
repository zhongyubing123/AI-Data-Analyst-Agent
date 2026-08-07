from services.sql_generator import generate_sql


MAX_RETRY = 2


def retry_sql(
        question,
        error,
        context
):

    """
    SQL自动修复
    """

    retry_prompt = f"""

原始问题:
{question}


之前生成SQL执行失败。

错误信息:
{error}


数据库Schema:
{context}


请重新生成正确SQL。

要求:
1. 只能使用Schema中的字段
2. 只能SELECT
3. 不要解释
4. 只返回SQL
5. 保持用户原始查询意图不变
6. 修复字段错误，不要删除原SQL需要返回的信息
7. 返回字段必须满足用户问题

"""


    sql = generate_sql(
        retry_prompt,
        context=context
    )


    return sql
   