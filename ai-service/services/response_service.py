from services.deepseek_service import chat


def generate_answer(data, message):

    if data is None:

        response = chat(message)

    else:

        response = chat(
f"""
数据库结果:

{data}

用户问题:

{message}

根据数据库结果回答。
不要编造。
"""
        )

    return response["content"]