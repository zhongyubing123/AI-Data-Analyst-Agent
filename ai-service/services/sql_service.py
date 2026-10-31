import re

from decimal import Decimal

from services.sql_guard import check_sql
from services.schema_guard import check_fields
from services.sql_generator import generate_sql
from services.sql_retry import retry_sql
from tools.mysql_tool import execute_query
from services.memory_service import save_context, get_sql_context


def extract_table(sql):

    match = re.search(r"from\s+(\w+)", sql, re.I)

    return match.group(1) if match else None


def decimal_to_float(rows):

    if not rows or isinstance(rows, dict):

        return rows

    for row in rows:

        for key, value in row.items():

            if isinstance(value, Decimal):

                row[key] = float(value)

    return rows


def validate(sql):

    """安全规则 + 字段存在性，两道都过才执行。"""

    result = check_sql(sql)

    if not result["safe"]:

        raise Exception(result["reason"])

    check_fields(sql)


def run_sql(message, intent, trace=None):

    sql = generate_sql(message, context=get_sql_context(), trace=trace)

    if sql == "NO_AVAILABLE_FIELD":

        return {"error": "NO_AVAILABLE_FIELD"}

    try:

        validate(sql)

        data = decimal_to_float(execute_query(sql))

    except Exception as first_error:

        try:

            sql = retry_sql(
                message,
                str(first_error),
                get_sql_context(),
                trace=trace
            )

            validate(sql)

            data = decimal_to_float(execute_query(sql))

        except Exception as retry_error:

            raise Exception(f"SQL执行失败:{retry_error}")

    save_context(
        data=data,
        intent=intent,
        sql=sql,
        table=extract_table(sql)
    )

    if trace is not None:

        trace.add("sql", sql)

        trace.add("rows", len(data) if isinstance(data, list) else 0)

    return {"sql": sql, "data": data}
