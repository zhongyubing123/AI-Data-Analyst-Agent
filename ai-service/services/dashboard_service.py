"""看板四个接口的数据查询。

原来这套在 Spring Boot 里，用 Java + MyBatis 查同样四张表。
现在改由 FastAPI 提供，前端调用方式不变（字段名用驼峰，和原来一致）。
"""

from tools.mysql_tool import execute_query
from services.sql_service import decimal_to_float


BRAND_SQL = """
SELECT brand,
       sales_amount AS salesAmount,
       buy_count    AS buyCount
FROM dws_brand_sales
ORDER BY sales_amount DESC
LIMIT 20
"""

CATEGORY_SQL = """
SELECT category,
       sales_amount AS salesAmount,
       buy_count    AS buyCount
FROM dws_category_sales
ORDER BY sales_amount DESC
LIMIT 20
"""

ITEM_SQL = """
SELECT item_id     AS itemId,
       item_name   AS itemName,
       pv_count    AS pvCount,
       fav_count   AS favCount,
       cart_count  AS cartCount,
       buy_count   AS buyCount
FROM dws_item_hot
ORDER BY buy_count DESC
LIMIT 20
"""

USER_SQL = """
SELECT user_id AS userId,
       pv_count + fav_count + cart_count + buy_count AS behaviorCount,
       buy_count AS buyCount
FROM dws_user_value
ORDER BY behaviorCount DESC
LIMIT 20
"""


def _rows(sql):

    return decimal_to_float(execute_query(sql))


def brand_sales():

    return _rows(BRAND_SQL)


def category_sales():

    return _rows(CATEGORY_SQL)


def item_hot():

    return _rows(ITEM_SQL)


def user_active():

    return _rows(USER_SQL)
