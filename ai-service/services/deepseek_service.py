from pathlib import Path

from services.llm_call import chat_completion
from services.conversation_memory import get_history, add_message


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "system_prompt.txt"
)

SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


def chat(message: str, trace=None):

    """普通对话，带最近两轮历史，返回 {"content", "usage"}。"""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    messages.extend(get_history())

    messages.append({"role": "user", "content": message})

    answer, usage = chat_completion(
        messages,
        trace=trace,
        temperature=0.2,
        max_tokens=200
    )

    add_message("user", message)
    add_message("assistant", answer)

    return {"content": answer, "usage": usage}
