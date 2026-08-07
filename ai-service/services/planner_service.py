import json
import logging
from pathlib import Path

from services.llm_client import client


logger = logging.getLogger(__name__)


PROMPT_PATH = (
    Path(__file__).parent.parent
    / "prompts"
    / "planner_prompt.txt"
)


PLANNER_PROMPT = (
    PROMPT_PATH
    .read_text(
        encoding="utf-8"
    )
)



def planner(message: str) -> dict:


    response = client.chat.completions.create(

        model="deepseek-chat",

        temperature=0,

        response_format={
            "type":"json_object"
        },

        messages=[

            {
                "role":"system",
                "content":PLANNER_PROMPT
            },

            {
                "role":"user",
                "content":message
            }

        ]

    )


    content = (
        response
        .choices[0]
        .message
        .content
    )


    try:

        result = json.loads(content)


        logger.info(
            "Planner result=%s",
            result
        )


        return result



    except json.JSONDecodeError:


        logger.error(
            "Planner JSON error:%s",
            content
        )


        return {

            "intent":"chat",

            "reason":
            "Planner解析失败"

        }