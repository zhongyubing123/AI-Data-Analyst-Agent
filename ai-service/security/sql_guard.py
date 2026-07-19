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
    """SQL安全检查，只允许执行SELECT查询"""

    if not sql:
        return {"safe": False, "reason": "SQL为空"}

    sql = sql.strip().upper()

    # 只允许 SELECT
    if not sql.startswith("SELECT"):
        return {"safe": False, "reason": "只允许执行SELECT"}

    # 禁止危险关键字
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql):
            return {"safe": False, "reason": f"禁止执行 {keyword}"}

    # 禁止查看数据库结构
    if any(cmd in sql for cmd in FORBIDDEN_COMMANDS):
        return {"safe": False, "reason": "禁止查看数据库结构"}

    # 禁止 DESC table
    if re.match(r"^DESC\s+\w+", sql):
        return {"safe": False, "reason": "禁止执行DESC"}

    # SELECT * 必须带 LIMIT
    if re.search(r"SELECT\s+\*", sql) and "LIMIT" not in sql:
        return {"safe": False, "reason": "SELECT * 必须添加LIMIT"}

    return {"safe": True, "reason": "通过"}