"""意图路由：先用关键词判断，判断不了才交给模型。

大多数问题靠规则就能定，省掉 planner 那一次调用（约 800 token）。
"""

import os

from services.planner_service import planner


CHART_WORDS = ("画", "图表", "柱状", "折线", "饼图", "趋势图", "可视化")

SQL_WORDS = (
    "销量", "销售额", "卖了多少", "金额", "排行", "排名", "top", "前十",
    "最高", "最多", "最少", "占比", "转化", "客单价", "复购", "活跃",
    "多少", "几个", "趋势", "每天", "每日", "分布",
    "建议", "优化", "怎么提升", "如何提升", "怎么办"
)

RAG_WORDS = (
    "什么是", "是什么", "什么意思", "含义", "为什么", "怎么实现",
    "架构", "原理"
)

CHAT_WORDS = ("你好", "你是谁", "能做什么", "hello", "hi")


def by_rule(message):
    """命中返回意图，判断不了返回 None。"""

    text = (message or "").lower().strip()

    if not text:
        return "chat"

    if any(word in text for word in CHAT_WORDS):
        return "chat"

    if any(word in text for word in CHART_WORDS):
        return "chart"

    if any(word in text for word in SQL_WORDS):
        return "sql"

    if any(word in text for word in RAG_WORDS):
        return "rag"

    return None


def route(message, trace=None):
    """返回 {"intent": ..., "by": "rule" 或 "model"}。

    环境变量 ROUTE=model 时跳过规则，全部交给模型，用于消融对比。
    """

    if os.getenv("ROUTE") == "model":

        result = planner(message, trace=trace)

        return {"intent": result.get("intent", "chat"), "by": "model"}

    intent = by_rule(message)

    if intent:

        if trace is not None:
            trace.add("route", "rule")

        return {"intent": intent, "by": "rule"}

    result = planner(message)

    if trace is not None:
        trace.add("route", "model")

    return {"intent": result.get("intent", "chat"), "by": "model"}
