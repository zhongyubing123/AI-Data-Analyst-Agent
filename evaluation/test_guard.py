"""SQL 安全规则的离线自测，不连库、不调模型。

    python evaluation/test_guard.py

12 条危险语句必须全部拦下，3 条正常查询必须放行，任何一条不符合就报错退出。
"""

import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / "ai-service"))


from services.sql_guard import check_sql  # noqa: E402


DANGEROUS = [
    "DELETE FROM dws_item_hot",
    "UPDATE dws_brand_sales SET sales_amount=0",
    "INSERT INTO dws_user_active VALUES (1,2)",
    "DROP TABLE dws_item_hot",
    "ALTER TABLE dws_item_hot ADD COLUMN note VARCHAR(20)",
    "TRUNCATE TABLE dws_brand_sales",
    "REPLACE INTO dws_brand_sales VALUES ('a',1,2)",
    "SELECT brand FROM dws_brand_sales; DROP TABLE dws_item_hot",
    "SELECT * FROM dws_item_hot",
    "SHOW TABLES",
    "DESCRIBE dws_item_hot",
    "DESC dws_item_hot"
]

NORMAL = [
    "SELECT brand, sales_amount FROM dws_brand_sales ORDER BY sales_amount DESC LIMIT 5",
    "SELECT COUNT(*) AS total FROM dws_item_hot",
    "SELECT item_name, pv_count FROM dws_item_hot LIMIT 20"
]


def main():

    failed = 0

    for sql in DANGEROUS:

        result = check_sql(sql)

        if result["safe"]:

            failed += 1

            print("应该拦下却没拦:", sql)

        else:

            print("拦下 [%s] %s" % (result["reason"], sql[:40]))

    for sql in NORMAL:

        result = check_sql(sql)

        if not result["safe"]:

            failed += 1

            print("正常查询被误杀:", sql, result["reason"])

    if failed:

        print("\n失败 %d 条" % failed)

        sys.exit(1)

    print("\n通过：危险 %d 条全拦，正常 %d 条放行"
          % (len(DANGEROUS), len(NORMAL)))


if __name__ == "__main__":
    main()
