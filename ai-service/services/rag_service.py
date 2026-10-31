from services.vector_search import search
from services.deepseek_service import chat


def build_prompt(context, message):

    return f"""企业知识：
{context}

问题：{message}

只根据上面的知识回答，知识里没有就说无法确定，不要编造。三句话内。
"""


def run_rag(message, trace=None):

    docs = search(message)

    if not docs:
        return "知识库里没有相关内容。"

    context = "\n".join(docs[:3])

    return chat(build_prompt(context, message), trace=trace)["content"]
