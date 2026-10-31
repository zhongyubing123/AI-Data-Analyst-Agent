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

    """SQL安全检查，只允许 SELECT。

    顺序有讲究：SHOW / DESC 这类语句本身不以 SELECT 开头，
    如果先判 SELECT，它们会被"只允许执行SELECT"拦下，
    后面两条更具体的原因永远走不到。
    """

    if not sql:

        return {"safe": False, "reason": "SQL为空"}

    sql = sql.strip().upper()

    # 多条语句拼接
    if ";" in sql[:-1]:

        return {"safe": False, "reason": "禁止执行多SQL语句"}

    # 查看库结构的命令
    if any(cmd in sql for cmd in FORBIDDEN_COMMANDS):

        return {"safe": False, "reason": "禁止查看数据库结构"}

    if re.match(r"^DESC\s+\w+", sql):

        return {"safe": False, "reason": "禁止执行DESC"}

    # 写操作关键字
    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(rf"\b{keyword}\b", sql):

            return {"safe": False, "reason": f"禁止执行 {keyword}"}

    # 只允许查询
    if not re.match(r"^SELECT\b", sql):

        return {"safe": False, "reason": "只允许执行SELECT"}

    if re.search(r"SELECT\s+\*", sql) and "LIMIT" not in sql:

        return {"safe": False, "reason": "SELECT * 必须添加LIMIT"}

    return {"safe": True, "reason": "通过"}
