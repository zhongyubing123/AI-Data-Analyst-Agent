"""评测：跑用例，按表名、关键词、数字、图表结构、禁用词判定。

用法：
    $env:MODE="fast"; $env:CASES="test_cases.json"; python evaluation/evaluator.py
    $env:MODE="full"; $env:CASES="test_cases.json"; python evaluation/evaluator.py

环境变量：
    MODE   fast 只测语句生成，full 走完整链路
    CASES  用例文件名，默认 test_cases.json
    LIMIT  只跑前 N 条，调试用
"""

import json
import os
import re
import sys
import time

from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE / "ai-service"))


from services.sql_generator import generate_sql  # noqa: E402
from services.agent_service import run_agent  # noqa: E402


MODE = os.getenv("MODE", "full")

CASES = os.getenv("CASES", "test_cases.json")

LIMIT = int(os.getenv("LIMIT", "0"))

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def load_cases():

    path = Path(__file__).resolve().parent / CASES

    cases = json.loads(path.read_text(encoding="utf-8"))

    return cases[:LIMIT] if LIMIT else cases


def ask(question):
    """返回 (用于判定的文本, 结构化结果)。"""

    if MODE == "fast":

        sql = generate_sql(question) or ""

        return sql, {"sql": sql}

    result = run_agent(question)

    text = "%s %s" % (result.get("answer") or "", result.get("sql") or "")

    return text, result


def judge(case, text, result):

    rule = case.get("assert") or {}

    reasons = []

    low = text.lower()

    table = rule.get("table")

    if table and table.lower() not in low:

        reasons.append("表不对，应为 %s" % table)

    for word in rule.get("keywords", []):

        if word.lower() not in low:

            reasons.append("缺关键词 %s" % word)

    for word in rule.get("forbid", []):

        if word.lower() in low:

            reasons.append("出现禁用词 %s" % word)

    if rule.get("expect_no_sql"):

        sql = (result.get("sql") or "").strip()

        # NO_AVAILABLE_FIELD 就是拒绝的标记，不算生成了 SQL
        if sql and sql != "NO_AVAILABLE_FIELD":

            reasons.append("应该拒绝生成 SQL，实际生成了")

    if MODE == "full" and rule.get("has_number"):

        answer = result.get("answer") or ""

        if not re.search(r"\d", answer):

            reasons.append("回答里没有数字")

    if MODE == "full" and rule.get("chart"):

        chart = result.get("chart")

        if not isinstance(chart, dict) or "series" not in chart:

            reasons.append("没有返回有效图表")

    return (not reasons), reasons


def main():

    cases = load_cases()

    rows = []

    passed = 0

    skipped = 0

    started = time.time()

    for case in cases:

        # fast 模式只测语句生成，图表、知识问答、建议在 full 模式里测
        if MODE == "fast" and case.get("type") != "sql":

            skipped += 1

            continue

        begin = time.time()

        try:

            text, result = ask(case["question"])

            ok, reasons = judge(case, text, result)

        except Exception as error:

            ok, reasons = False, ["异常: %s" % error]

            text = ""

        cost = round(time.time() - begin, 2)

        passed += 1 if ok else 0

        rows.append({
            "id": case.get("id"),
            "type": case.get("type"),
            "question": case["question"],
            "pass": ok,
            "reasons": reasons,
            "seconds": cost,
            "text": text[:200]
        })

        print(("OK   " if ok else "FAIL ") + "%s %s" % (case.get("id"), case["question"]))

        for reason in reasons:

            print("        " + reason)

    total = len(rows)

    accuracy = round(passed / total, 4) if total else 0

    summary = {}

    for row in rows:

        bucket = summary.setdefault(row["type"], {"total": 0, "pass": 0})

        bucket["total"] += 1

        bucket["pass"] += 1 if row["pass"] else 0

    elapsed = round(time.time() - started, 1)

    print("\n模式 %s，用例 %s，跳过 %d，用时 %s 秒" % (MODE, CASES, skipped, elapsed))
    print("总准确率 %s（%d / %d）" % (accuracy, passed, total))

    for name, bucket in sorted(summary.items()):

        rate = round(bucket["pass"] / bucket["total"], 4)

        print("  %s：%s（%d / %d）" % (name, rate, bucket["pass"], bucket["total"]))

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stem = Path(CASES).stem

    out = RESULTS_DIR / ("%s_%s.json" % (MODE, stem))

    out.write_text(
        json.dumps({
            "mode": MODE,
            "cases": CASES,
            "accuracy": accuracy,
            "passed": passed,
            "total": total,
            "skipped": skipped,
            "seconds": elapsed,
            "summary": summary,
            "results": rows
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("结果写入 %s" % out)


if __name__ == "__main__":
    main()
