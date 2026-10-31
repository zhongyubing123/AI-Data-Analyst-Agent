import json
import logging

from pathlib import Path

from services.llm_call import chat_completion


logger = logging.getLogger(__name__)

PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "planner_prompt.txt"
)

PLANNER_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


def planner(message: str, trace=None):

    """规则判断不了时才调，做一次四分类。"""

    content, _ = chat_completion(
        [
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": message}
        ],
        trace=trace,
        temperature=0,
        response_format={"type": "json_object"},
        max_tokens=30
    )

    try:

        result = json.loads(content)

        return {"intent": result.get("intent", "chat")}

    except json.JSONDecodeError:

        logger.warning("planner 返回的不是 JSON: %s", content)

        return {"intent": "chat"}
