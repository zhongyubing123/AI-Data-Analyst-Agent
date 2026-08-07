import json

from services.llm_client import client



def clean_json(content):

    return (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )



def validate_chart(option):

    required = [
        "title",
        "xAxis",
        "yAxis",
        "series"
    ]

    return all(
        key in option
        for key in required
    )



def generate_chart(data, question):
    """
    根据数据库结果生成 ECharts 配置
    """


    if not data:

        return None



    prompt = f"""

你是一名企业级数据可视化工程师。


根据下面的数据生成 ECharts Option。


用户需求：

{question}


数据：

{data}


要求：

1. 只返回JSON

2. 不要Markdown

3. 必须包含：

title

xAxis

yAxis

series

4. series必须使用真实数据

5. 不要编造不存在的数据

"""


    response = client.chat.completions.create(

        model="deepseek-chat",

        temperature=0,

        messages=[

            {
                "role":"user",
                "content":prompt
            }

        ]

    )



    content = clean_json(
        response
        .choices[0]
        .message
        .content
    )



    try:

        option = json.loads(content)



        if not validate_chart(option):

            return {
                "error":
                "ECharts结构不完整",
                "raw":
                option
            }



        return option



    except json.JSONDecodeError:


        return {

            "error":
            "图表JSON解析失败",

            "raw":
            content

        }