from pathlib import Path
import json

from services.llm_client import client
from services.memory import get_history, add_message



# 加载 Prompt

PROMPT_PATH = (
    Path(__file__).parent.parent
    / "prompts"
    / "planner_prompt.txt"
)


with open(
    PROMPT_PATH,
    "r",
    encoding="utf-8"
) as f:

    PLANNER_PROMPT = f.read()



def planner(message: str):


    messages = [

        {
            "role":"system",
            "content":PLANNER_PROMPT
        }

    ]


    # 加入历史上下文

    messages.extend(
        get_history()
    )


    # 当前问题

    messages.append(
        {
            "role":"user",
            "content":message
        }
    )



    response = client.chat.completions.create(

        model="deepseek-chat",

        temperature=0,

        response_format={
            "type":"json_object"
        },

        messages=messages

    )


    try:


        result=json.loads(
            response.choices[0].message.content
        )


        # 保存Planner上下文

        add_message(
            "user",
            message
        )


        add_message(
            "assistant",
            json.dumps(
                result,
                ensure_ascii=False
            )
        )


        return result



    except Exception:


        return {

            "intent":"chat",

            "table":"",

            "reason":"Planner解析失败"

        }