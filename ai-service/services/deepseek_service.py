from pathlib import Path

from services.llm_client import client
from services.conversation_memory import get_history, add_message


PROMPT_PATH = (
    Path(__file__).parent.parent
    / "prompts"
    / "system_prompt.txt"
)


with open(
    PROMPT_PATH,
    "r",
    encoding="utf-8"
) as f:

    SYSTEM_PROMPT = f.read()



def chat(message: str):


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]


    # 添加历史上下文

    messages.extend(
        get_history()
    )


    messages.append(
        {
            "role": "user",
            "content": message
        }
    )



    response = client.chat.completions.create(

        model="deepseek-chat",

        temperature=0.2,

        messages=messages

    )



    answer = (
        response
        .choices[0]
        .message
        .content
    )



    # ======================
    # Token统计
    # ======================

    usage = {

        "prompt_tokens":
            response.usage.prompt_tokens,

        "completion_tokens":
            response.usage.completion_tokens,

        "total_tokens":
            response.usage.total_tokens

    }



    # 保存最终回答

    add_message(
        "user",
        message
    )


    add_message(
        "assistant",
        answer
    )



    return {

        "content": answer,

        "usage": usage

    }