from services.deepseek_service import chat


# 命中这些词，回答改成"现象 / 推测 / 建议 / 参照"四段
ADVICE_WORDS = (
    "建议", "优化", "怎么提升", "如何提升",
    "怎么办", "改进", "怎么改善"
)


def is_advice(message):

    return any(word in message for word in ADVICE_WORDS)


def build_answer_prompt(data, message):

    return f"数据：{data}\n\n问题：{message}\n\n按数据回答，三句话内，不要编造。"


def build_advice_prompt(data, message):

    return f"""数据：{data}

问题：{message}

按下面四段回答，每段一行，总字数不超过 150 字：
现象：用数据说话，必须带数字
推测：一句可能的原因，开头写"推测"
建议：一条能落地的动作，不要空话
参照：和均值或最高值比一句

没有数据支撑的话不要写，不要引入外部信息。
"""


def generate_answer(data, message, trace=None):

    if data is None:

        return chat(message, trace=trace)["content"]

    prompt = (
        build_advice_prompt(data, message)
        if is_advice(message)
        else build_answer_prompt(data, message)
    )

    return chat(prompt, trace=trace)["content"]
