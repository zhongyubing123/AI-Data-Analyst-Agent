import json

from services.llm_call import chat_completion


REQUIRED_KEYS = ("title", "xAxis", "yAxis", "series")


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

    return f"""数据：{data}

需求：{question}

只输出一个 JSON 对象，包含 title、xAxis、yAxis、series 四个键，
series 必须使用上面的真实数据，不要编造。不要 Markdown。
"""


def generate_chart(data, question, trace=None):
    """把查询结果翻成 ECharts 配置，失败返回带 error 的字典。"""

    if not data:
        return None

    content, _ = chat_completion(
        [{"role": "user", "content": build_prompt(data, question)}],
        trace=trace,
        temperature=0,
        max_tokens=500
    )

    content = clean_json(content)

    try:

        option = json.loads(content)

    except json.JSONDecodeError:

        return {"error": "图表JSON解析失败", "raw": content}

    if not validate_chart(option):

        return {"error": "ECharts结构不完整", "raw": option}

    return option
