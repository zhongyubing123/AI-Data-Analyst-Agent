"""统一的大模型调用入口。

四个模块原来各写一遍 client.chat.completions.create，
收敛到这里之后，换模型、取 usage 都只改一个地方。
"""

from services.llm_client import client


MODEL = "deepseek-chat"


def chat_completion(messages, trace=None, **kwargs):
    """调用一次模型，返回 (content, usage)。

    trace 不为空时把这次调用的 token 累加进去。
    """

    kwargs.setdefault("model", MODEL)

    response = client.chat.completions.create(
        messages=messages,
        **kwargs
    )

    usage = None

    if getattr(response, "usage", None) is not None:

        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }

        if trace is not None:
            trace.add_token(usage)

    return response.choices[0].message.content, usage
