import re
from decimal import Decimal

from services.sql_guard import check_sql
from services.sql_generator import generate_sql
from services.sql_retry import retry_sql
from tools.mysql_tool import execute_query
from services.memory_service import (
    save_context,
    get_sql_context
)


def extract_table(sql):

    match = re.search(
        r"from\s+(\w+)",
        sql,
        re.I
    )

    return match.group(1) if match else None



def decimal_to_float(rows):

    if not rows:
        return rows


    for row in rows:

        for k, v in row.items():

            if isinstance(v, Decimal):

                row[k] = float(v)


    return rows



def run_sql(message, intent):


    sql = generate_sql(
        message,
        context=get_sql_context()
    )



    if sql == "NO_AVAILABLE_FIELD":

        return {
            "error": "NO_AVAILABLE_FIELD"
        }



    try:


        check_result = check_sql(sql)


        if not check_result["safe"]:

            raise Exception(
                check_result["reason"]
            )


        data = decimal_to_float(
            execute_query(sql)
        )



    except Exception as e:


        try:


            sql = retry_sql(

                message,

                str(e),

                get_sql_context()

            )


            check_result = check_sql(sql)


            if not check_result["safe"]:

                raise Exception(
                    check_result["reason"]
                )



            data = decimal_to_float(

                execute_query(sql)

            )



        except Exception as retry_error:


            raise Exception(
                f"SQL执行失败:{retry_error}"
            )



    save_context(

        data=data,

        intent=intent,

        sql=sql,

        table=extract_table(sql)

    )



    return {

        "sql": sql,

        "data": data

    }