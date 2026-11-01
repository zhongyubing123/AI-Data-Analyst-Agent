# 基于大模型的电商数据分析助手

用自然语言查电商数据：问一句话，系统生成 SQL、执行查询、把结果讲成人话，需要图时直接出图。

数据来自公开的电商用户行为数据集，经 ODS → DWD → DWS 三层加工成五张汇总表，模型只面对汇总层，不碰明细。

## 架构

```
Vue（对话 + 看板两个 tab）
  ↕
FastAPI
  ├─ 规则路由：关键词先判意图，判断不了才调模型
  ├─ 意图：sql / chart / rag / chat
  ├─ SQL：生成 → 安全校验 → 字段校验 → 执行 → 失败重试一次
  ├─ 记忆：Redis 存上一轮实体，支持"它""这个品牌"追问
  └─ 检索：知识库 Top-3，回答指标含义类问题
  ↕
MySQL（9 张表：ODS 1 + DWD 2 + DWS 6）
```

## 快速开始

```bash
# 1. 建库、导入、分层汇总（改一下 mysql_all.sql 里的 CSV 路径）
mysql --local-infile=1 --default-character-set=utf8mb4 -u root -p < sql/mysql_all.sql

# 2. 配 .env
cp ai-service/.env.example ai-service/.env    # 然后填 key 和密码

# 3. 起服务
cd ai-service
pip install -r requirements.txt
uvicorn app:app --reload

# 4. 起前端
cd vue
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`，两个 tab：智能问答、数据看板。

详细步骤见 `runbook/`，按 01 → 04 顺序执行。

## 目录

| 目录 | 内容 |
|---|---|
| `ai-service/` | FastAPI 服务：路由、SQL 生成与校验、记忆、检索、图表 |
| `vue/` | 前端：对话页、看板页、图表组件 |
| `sql/` | `mysql_all.sql` 一键建库导入；`hive_offline.sql` 是 Hive 版离线实现 |
| `runbook/` | 操作手册，照着敲就行 |
| `evaluation/` | 安全自测与三组评测用例 |
| `docs/` | 架构说明与迭代记录 |
| `extensions/` | 存档：旧数据、旧脚本、Spring Boot 版本 |

## 能回答的问题

- 哪个商品、品牌、品类卖得最好，卖了多少钱
- 商品客单价、品牌客单价、品类商品数
- 浏览多但买得少的商品（转化率低）
- 哪个价格带最好卖，转化率多少
- 每天成交额趋势、哪些用户消费最高、复购用户占比
- 画柱状图、饼图、折线图
- 指标含义、系统怎么做的

## 评测

```bash
python evaluation/test_guard.py          # 安全规则自测，不花钱
$env:MODE="fast"; $env:CASES="biz_cases.json"; python evaluation/evaluator.py
```

结果写在 `evaluation/results/`，文件名带模式和用例集，互不覆盖。

## 已知限制

- 数据是历史上的一段，问"最近一周"会查不到，按数据集内日期问
- 知识库靠人工维护，新增指标要同步补文档
- 只做只读查询，没有增量更新和调度
