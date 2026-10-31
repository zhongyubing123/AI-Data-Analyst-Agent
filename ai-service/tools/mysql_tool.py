import os

import pymysql
from dotenv import load_dotenv

from services.sql_guard import check_sql

load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset="utf8mb4"
    )


def execute_query(sql: str):
    check = check_sql(sql)

    if not check["safe"]:
        raise Exception(check["reason"])

    conn = get_connection()

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    finally:
        conn.close()