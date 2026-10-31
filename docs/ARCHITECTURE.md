# 系统结构

一页说明白：请求怎么走、每个文件干什么、哪些是核心。

## 一次提问的路径

```
Vue 对话页  ──POST /chat──▶  app.py
                               │
                               ▼
                     agent_service.run_agent
                     （计时、建 trace、按意图分发）
                               │
        ┌──────────────┬───────┴────────┬──────────────┐
        ▼              ▼                ▼              ▼
   resolve_context  planner          run_sql        run_rag
   指代补全          四类意图          生成→校验→执行   检索→拼上下文
        │              │             →重试→存记忆        │
        └──────────────┴────────┬───────┴──────────────┘
                                ▼
                        {answer, chart}
```

意图为 `chart` 时，`run_sql` 先取数，再由 `chart_service` 把数据翻成 ECharts 配置。

## 模块职责

| 文件 | 职责 | 是不是核心 |
|---|---|---|
| `app.py` | 两个接口：探活、对话 | 核心 |
| `services/agent_service.py` | 编排：计时、分发、组装返回 | 核心 |
| `services/planner_service.py` | 意图分类（sql / chart / rag / chat） | 核心 |
| `services/sql_generator.py` | 注入字段清单，生成 SELECT | 核心 |
| `services/sql_guard.py` | 七条规则，拦写操作与库结构查询 | 核心 |
| `services/sql_service.py` | 生成、校验、执行、重试、落记忆 | 核心 |
| `services/memory_service.py` | Redis 存上一轮实体，做指代补全 | 核心 |
| `services/rag_service.py` + `vector_search.py` | 检索三段，交给模型作答 | 核心 |
| `services/chart_service.py` | 数据转 ECharts 配置 | 核心 |
| `services/llm_call.py` | 唯一的大模型调用入口 | 基建 |
| `services/trace_service.py` | 分步计时、token 累加、写日志 | 基建 |
| `tools/mysql_tool.py` | 连库、执行、执行前再校验一次 | 基建 |
| `services/conversation_memory.py` | 进程内聊天历史（只给普通对话用） | 基建 |
| `services/build_vector.py` | 建知识库索引的脚本，不参与运行 | 工具 |
| `backend/` | Spring Boot 看板接口，独立部署 | 配套 |
| `vue/` | 对话页与看板页 | 配套 |
| `etl/` + `sql/` | 离线加工与建表 | 数据侧 |

## 三条容易混淆的边界

1. **两套后端**：对话链路走 FastAPI，看板链路走 Spring Boot，互不依赖。
2. **两处记忆**：Redis 存业务实体（给指代补全用），进程内列表存聊天历史（给普通对话用），不要合并。
3. **两道校验**：`sql_guard` 管"不许做什么"，`mysql_tool` 在执行前再查一次；字段存不存在由 `schema.txt` 的清单约束。

## 启动

```bash
cd ai-service
pip install -r requirements.txt
uvicorn app:app --reload
```

需要 `.env` 里配好 `DEEPSEEK_API_KEY`、`MYSQL_*`。

## 评测

```bash
python evaluation/evaluator.py                    # 完整链路 10 条
python evaluation/evaluator.py                    # 改 MODE 为 fast 跑 20 条
```

结果写到 `evaluation/results/{MODE}_results.json`，两个模式互不覆盖。
