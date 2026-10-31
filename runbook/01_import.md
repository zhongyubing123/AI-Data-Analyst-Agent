# 1. 导入数据与分层建表

一条命令建完所有表：ODS 原始表、DWD 两张、DWS 六张汇总表。

## 1.1 改 CSV 路径

打开 `sql/mysql_all.sql`，找到：

```sql
LOAD DATA LOCAL INFILE 'D:/data/user_behavior.csv'
```

改成你 CSV 的实际路径。CSV 要有表头，第一行会被 `IGNORE 1 LINES` 跳过。

## 1.2 执行

```bash
cd C:\Users\zhong\Desktop\AI-Data-Analyst-Agent
mysql --local-infile=1 --default-character-set=utf8mb4 -u root -p < sql\mysql_all.sql
```

跑完会打印一份自检表，八行数字：

```
ods     69000
fact    69000
item     3000
brand      20
category    8
price_band  4
daily      30
user    20000
```

行数按你的数据实际值，关键是 `ods` 和 `fact` 相等、`dws_item_hot` 不为 0。

## 1.3 检查有没有数

```sql
USE ecommerce;

SELECT brand, sales_amount FROM dws_brand_sales ORDER BY sales_amount DESC LIMIT 5;
SELECT item_name, buy_count, sales_amount FROM dws_item_hot ORDER BY sales_amount DESC LIMIT 5;
SELECT dt, sales_amount FROM dws_daily_trend ORDER BY dt LIMIT 3;
```

销售额全是 0：CSV 的 `price` 列没读进来，检查表头顺序是不是和 `ods_user_behavior` 一致。

中文变问号：执行时漏了 `--default-character-set=utf8mb4`，重跑一遍。

`dt` 是空的：CSV 里没有时间列，用时间戳补：

```sql
UPDATE ods_user_behavior
SET dt = FROM_UNIXTIME(ts) WHERE dt IS NULL OR dt = '';
```

然后从 `fact_behavior` 那一步开始重跑。

## 1.4 想重来

脚本开头是 `DROP TABLE IF EXISTS`，直接重跑就是全量重建。数据小，几十秒的事。
