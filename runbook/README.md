# 运行手册

一套 MySQL 跑完全部，不分机器、不搬数据。

| 顺序 | 文件 | 干什么 | 耗时 |
|---|---|---|---|
| 1 | `01_import.md` | 建库、导入 CSV、分层建表 | 10 分钟 |
| 2 | `02_service.md` | 装依赖、配 .env、起服务、试问 | 10 分钟 |
| 3 | `03_eval.md` | 安全自测与两组评测 | 15 分钟 |
| 4 | `04_token.md` | 看每次问答的 token | 5 分钟 |

前置：MySQL 8 在跑，Redis 在跑，`DEEPSEEK_API_KEY` 有余额。

分层没丢：`ods_user_behavior`（原始）→ `dim_goods`/`fact_behavior`（清洗）→ 五张 `dws_` 汇总表。
只是加工从 Hive 换成了 MySQL 的 `INSERT ... SELECT`。Hive 版本留在 `sql/hive_offline.sql`，论文写离线链路时引用它。
