"""数据体检：查一遍行为分布和汇总表，确认导入有没有错位。

用法（在 ai-service 目录下）：
    python check_data.py
"""

import os

import pymysql

from dotenv import load_dotenv


load_dotenv()

QUERIES = [
    ("行为分布", "SELECT behavior, COUNT(*) AS cnt FROM ods_user_behavior GROUP BY behavior"),
    ("商品表合计", "SELECT SUM(pv_count) AS pv, SUM(fav_count) AS fav, "
                   "SUM(cart_count) AS cart, SUM(buy_count) AS buy FROM dws_item_hot"),
    ("购买最多的商品", "SELECT item_name, pv_count, buy_count FROM dws_item_hot "
                       "ORDER BY buy_count DESC LIMIT 5"),
    ("浏览大于购买的商品数", "SELECT COUNT(*) AS cnt FROM dws_item_hot WHERE pv_count > buy_count"),
]


def main():

    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "ecommerce"),
        charset="utf8mb4"
    )

    try:

        for title, sql in QUERIES:

            print("=" * 12, title)

            with conn.cursor() as cur:

                cur.execute(sql)

                columns = [item[0] for item in cur.description]

                print(" | ".join(columns))

                for row in cur.fetchall():

                    print(" | ".join(str(value) for value in row))

            print()

    finally:

        conn.close()


if __name__ == "__main__":
    main()
