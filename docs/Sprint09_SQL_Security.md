# Sprint09：AI Agent SQL Security Enhancement


> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


在 AI Data Analyst Agent 基础上，增加 SQL 安全检查机制。


由于系统已经支持：

- NL2SQL
- 自动生成 SQL
- MySQL 查询


因此需要在 SQL 执行前增加安全校验，避免 AI 生成危险数据库操作。


本 Sprint 目标：

实现 SQL Guard，对 AI 生成 SQL 进行检测，只允许执行数据查询操作。


---


# Background


当前流程：

