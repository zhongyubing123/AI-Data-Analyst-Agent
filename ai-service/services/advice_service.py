"""建议类问题的兜底取数。

"给点运营建议"这种问题没有具体指标，SQL 生成环节会返回 NO_AVAILABLE_FIELD。
这里改成固定查两组概览数据（品类销售、价格带转化），再让模型基于这两组给建议。
不猜、不编，永远有数据可依。
"""

from tools.mysql_tool import execute_query
from services.sql_service import decimal_to_float
from services.deepseek_service import chat


CATEGORY_SQL = """
SELECT category, sales_amount, buy_count, avg_amount
FROM dws_category_sales
ORDER BY sales_amount DESC
LIMIT 5
"""

BRAND_SQL = """
SELECT brand, sales_amount, buyer_count
FROM dws_brand_sales
ORDER BY sales_amount DESC
LIMIT 5
"""


def _rows(sql):

    return decimal_to_float(execute_query(sql))


def run_advice(message, trace=None):

    categories = _rows(CATEGORY_SQL)

    brands = _rows(BRAND_SQL)

    prompt = f"""品类销售前五：
{categories}

品牌销售前五：
{brands}

问题：{message}

按下面四段回答，每段一行，总字数不超过 150 字：
现象：引用上面的数字，金额超过一万用万元表示，保留一位小数
推测：一句可能原因，开头写"推测"
建议：一条能落地的动作，不要空话
参照：和最高值或均值比一句

只能用上面的数据，不要编造。
"""

    answer = chat(prompt, trace=trace)["content"]

    return {
        "answer": answer,
        "chart": None,
        "sql": CATEGORY_SQL.strip(),
        "rows": len(categories) + len(brands)
    }
