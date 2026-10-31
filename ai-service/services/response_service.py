from services.deepseek_service import chat


def generate_answer(data, message, trace=None):

    if data is None:

        return chat(message, trace=trace)["content"]

    prompt = f"数据：{data}\n\n问题：{message}\n\n按数据回答，三句话内。"

    return chat(prompt, trace=trace)["content"]
