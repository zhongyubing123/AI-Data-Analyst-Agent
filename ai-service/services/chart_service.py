import json

from services.llm_call import chat_completion


REQUIRED_KEYS = ("title", "xAxis", "yAxis", "series")

# 行数太多会让模型输出的 JSON 被截断，画图用前 30 行足够
MAX_ROWS = 30


def clean_json(content):

    return (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


def validate_chart(option):

    return all(key in option for key in REQUIRED_KEYS)


def build_prompt(data, question):

    rows = data[:MAX_ROWS] if isinstance(data, list) else data

    total = len(data) if isinstance(data, list) else 0

    return f"""你只输出 JSON，不要输出 SQL，不要解释，不要 Markdown 代码块。

数据（共 {total} 行，以下是前 {len(rows)} 行）：{rows}

需求：{question}

输出一个 ECharts 配置对象，必须包含 title、xAxis、yAxis、series 四个键，
series 使用上面的真实数据，第一个字符必须是花括号。金额统一除以一万，按万元显示并保留一位小数；类目超过八个时只取前八个。
"""


def generate_chart(data, question, trace=None):
    """把查询结果翻成 ECharts 配置，失败返回带 error 的字典。"""

    if not data:
        return None

    content, _ = chat_completion(
        [{"role": "user", "content": build_prompt(data, question)}],
        trace=trace,
        temperature=0,
        max_tokens=900
    )

    content = clean_json(content)

    try:

        option = json.loads(content)

    except json.JSONDecodeError:

        return {"error": "图表JSON解析失败", "raw": content}

    if not validate_chart(option):

        return {"error": "ECharts结构不完整", "raw": option}

    return option
