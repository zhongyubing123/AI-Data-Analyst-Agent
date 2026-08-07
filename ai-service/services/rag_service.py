from services.vector_search import search
from services.deepseek_service import chat




def run_rag(message):


    docs = search(message)



    if not docs:

        return "未找到相关企业知识。"



    context = "\n".join(
        docs[:3]
    )



    response = chat(

        f"""

企业知识：

{context}


用户问题：

{message}


回答要求：

1. 根据企业知识回答

2. 如果知识中没有答案，
   明确说明无法确定

3. 不要编造信息

"""

    )



   


    return response["content"]