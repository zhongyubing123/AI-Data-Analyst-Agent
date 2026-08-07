import re


FORBIDDEN_KEYWORDS = (
    "DELETE",
    "UPDATE",
    "INSERT",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "REPLACE"
)


FORBIDDEN_COMMANDS = (
    "SHOW TABLES",
    "SHOW COLUMNS",
    "DESCRIBE"
)



def check_sql(sql: str):

    """
    SQL安全检查，只允许SELECT
    """


    if not sql:

        return {
            "safe":False,
            "reason":"SQL为空"
        }



    sql = sql.strip().upper()



    # 禁止多SQL
    if ";" in sql[:-1]:

        return {
            "safe":False,
            "reason":"禁止执行多SQL语句"
        }



    # 只允许SELECT

    if not re.match(
        r"^SELECT\b",
        sql
    ):

        return {
            "safe":False,
            "reason":"只允许执行SELECT"
        }



    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(
            rf"\b{keyword}\b",
            sql
        ):

            return {
                "safe":False,
                "reason":
                f"禁止执行 {keyword}"
            }



    if any(
        cmd in sql
        for cmd in FORBIDDEN_COMMANDS
    ):

        return {
            "safe":False,
            "reason":
            "禁止查看数据库结构"
        }



    if re.match(
        r"^DESC\s+\w+",
        sql
    ):

        return {
            "safe":False,
            "reason":
            "禁止执行DESC"
        }



    if (
        re.search(
            r"SELECT\s+\*",
            sql
        )
        and
        "LIMIT" not in sql
    ):

        return {
            "safe":False,
            "reason":
            "SELECT * 必须添加LIMIT"
        }



    return {
        "safe":True,
        "reason":"通过"
    }