"""执行前的字段存在性校验。

schema.txt 一行一张表：表 表名(字段, 字段, ...)
解析出来核对语句里的表和列，拦住模型跨表借用字段。
复杂语句解析不出来就放行，宁可漏拦，不误杀。
"""

import re

from pathlib import Path


SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "schema.txt"
)


class SchemaError(Exception):
    """表或字段不在清单里。"""


def load_schema(path=None):
    """返回 {表名: [字段名]}。"""

    path = Path(path or SCHEMA_PATH)

    tables = {}

    for raw in path.read_text(encoding="utf-8").splitlines():

        line = raw.strip()

        # 一行一张表：表 表名(a, b, c)
        match = re.match(
            r"^(?:表|table)\s*[:：]?\s*([\w\.]+)\s*\((.*)\)\s*$",
            line,
            re.I
        )

        if not match:

            continue

        name = match.group(1).strip().lower()

        fields = [
            item.strip().lower()
            for item in match.group(2).split(",")
            if item.strip()
        ]

        tables[name] = fields

    return tables


SCHEMA_FIELDS = load_schema()

ALL_FIELDS = {
    field
    for fields in SCHEMA_FIELDS.values()
    for field in fields
}


def _column_name(expr):
    """从 select 列表的一段里取列名，取不出来返回 None。"""

    expr = expr.strip()

    if not expr or expr == "*":

        return None

    if "(" in expr or any(ch in expr for ch in "'\""):

        return None

    expr = re.sub(r"\s+as\s+\w+$", "", expr, flags=re.I)

    return expr.split()[-1].split(".")[-1].strip("`").lower()


def check_fields(sql):
    """通过返回 True，不通过抛 SchemaError。"""

    if not sql:

        return True

    text = sql.strip().rstrip(";")

    tables = [
        name.strip("`").lower()
        for name in re.findall(
            r"\b(?:from|join)\s+([`\w\.]+)",
            text,
            re.I
        )
    ]

    unknown = [name for name in tables if name not in SCHEMA_FIELDS]

    if unknown:

        raise SchemaError(f"未知表: {unknown[0]}")

    select_part = re.search(r"\bselect\b(.*?)\bfrom\b", text, re.I | re.S)

    if not select_part:

        return True

    for expr in select_part.group(1).split(","):

        name = _column_name(expr)

        if not name:

            continue

        if name not in ALL_FIELDS:

            raise SchemaError(f"字段不存在: {name}")

        if len(tables) == 1 and name not in SCHEMA_FIELDS[tables[0]]:

            raise SchemaError(f"表 {tables[0]} 没有字段: {name}")

    return True
