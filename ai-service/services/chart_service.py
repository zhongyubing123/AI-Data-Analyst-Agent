import json

from services.llm_client import client


def generate_chart(data, question):
    """根据数据库结果生成 ECharts 配置"""

    prompt = f"""
你是一名企业级数据可视化工程师。

根据下面的数据生成 ECharts Option。

用户需求：
{question}

数据：
{data}

要求：
1. 只返回 JSON
2. 不要 Markdown
3. JSON 必须包含 title、xAxis、yAxis、series
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = (
        response.choices[0]
        .message.content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "error": "图表 JSON 解析失败",
            "raw": content
        }