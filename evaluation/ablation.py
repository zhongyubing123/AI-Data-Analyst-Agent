"""对比实验：同一批问题，换不同配置跑，比较 token、调用次数、正确率。

三组对比：
    baseline   规则路由 + 字段校验（默认）
    ROUTE=model  跳过关键词规则，每次都由模型判断意图
    GUARD=off    跳过字段存在性校验

用法：
    python evaluation/ablation.py
"""

import json
import os
import sys
import time

from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE / "ai-service"))


LOG_DIR = BASE / "ai-service" / "logs"

RESULTS = Path(__file__).resolve().parent / "results"

QUESTIONS = [
    ("哪个品类卖得最好", "dws_category_sales"),
    ("销售额前十的品牌", "dws_brand_sales"),
    ("哪个商品卖得最多", "dws_item_hot"),
    ("每天成交额是多少", "dws_daily_trend"),
    ("消费最高的十个用户", "dws_user_value"),
    ("每个品类有多少个商品", "dws_category_sales"),
    ("哪个品牌客单价最高", "dws_brand_sales"),
    ("收藏次数最多的商品", "dws_item_hot"),
    ("买过三次以上的用户有多少", "dws_user_value"),
    ("销量最高的前五个商品", "dws_item_hot"),
    ("买家数最多的品牌", "dws_brand_sales"),
    ("电子产品卖得怎么样", "dws_category_sales")
]

CONFIGS = [
    ("baseline", {}),
    ("ROUTE=model", {"ROUTE": "model"}),
    ("GUARD=off", {"GUARD": "off"})
]


def snapshot():

    if not LOG_DIR.exists():

        return set()

    return {item.name for item in LOG_DIR.glob("trace_*.json")}


def read_new(before):

    after = snapshot()

    fresh = []

    for name in after - before:

        try:

            data = json.loads((LOG_DIR / name).read_text(encoding="utf-8"))

        except Exception:

            continue

        fresh.append(data)

    return fresh


def run_one(name, env):
    """跑一组配置，返回统计结果。"""

    from services.agent_service import run_agent

    for key, value in env.items():

        os.environ[key] = value

    for key in ("ROUTE", "GUARD"):

        if key not in env:

            os.environ.pop(key, None)

    tokens = 0
    calls = 0
    errors = 0
    correct = 0

    for question, table in QUESTIONS:

        before = snapshot()

        sql = ""

        try:

            result = run_agent(question)

            sql = result.get("sql") or ""

            if table in sql.lower():

                correct += 1

        except Exception:

            errors += 1

        for data in read_new(before):

            tokens += int((data.get("token_usage") or {}).get("total_tokens") or 0)

            calls += int(data.get("llm_calls") or 0)

    n = len(QUESTIONS)

    return {
        "config": name,
        "accuracy": round(correct / n, 4),
        "avg_tokens": round(tokens / n, 1),
        "avg_calls": round(calls / n, 2),
        "errors": errors,
        "total_tokens": tokens
    }


def main():

    print("对比实验：%d 个问题 × %d 组配置\n" % (len(QUESTIONS), len(CONFIGS)))

    rows = []

    started = time.time()

    for name, env in CONFIGS:

        print("跑 %s ..." % name, end="", flush=True)

        row = run_one(name, env)

        rows.append(row)

        print(" 准确率 %s，平均 %s token，平均 %s 次调用，异常 %d"
              % (row["accuracy"], row["avg_tokens"], row["avg_calls"], row["errors"]))

    RESULTS.mkdir(parents=True, exist_ok=True)

    out = RESULTS / "ablation.json"

    out.write_text(
        json.dumps({
            "questions": len(QUESTIONS),
            "seconds": round(time.time() - started, 1),
            "rows": rows
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    base = rows[0]

    print("\n相对 baseline 的变化")
    for row in rows[1:]:

        token_delta = round((row["avg_tokens"] - base["avg_tokens"]) / base["avg_tokens"] * 100, 1) if base["avg_tokens"] else 0
        print("  %s：token %+.1f%%，调用 %+.2f 次，准确率 %+.2f"
              % (row["config"], token_delta,
                 row["avg_calls"] - base["avg_calls"],
                 row["accuracy"] - base["accuracy"]))

    print("\n结果写入 %s" % out)


if __name__ == "__main__":
    main()
