"""
上下文解析模块
负责处理：
它
这个
那个
第一名
第二名
上一条
等指代问题
"""


class ContextManager:

    def __init__(self):

        self.memory = {
            "last_intent": None,
            "last_table": None,
            "last_result": None,
            "last_entity": None
        }


    def update(
            self,
            intent=None,
            table=None,
            result=None
    ):

        if intent:
            self.memory["last_intent"] = intent

        if table:
            self.memory["last_table"] = table

        if result:
            self.memory["last_result"] = result


            # 保存第一个实体
            if isinstance(result,list):

                first = result[0]

                if "item_name" in first:

                    self.memory["last_entity"] = first["item_name"]

                elif "brand" in first:

                    self.memory["last_entity"] = first["brand"]



    def resolve(self,message):

        entity = self.memory.get(
            "last_entity"
        )


        if not entity:
            return message



        replace_words=[
            "它",
            "这个商品",
            "这个",
            "那个",
            "该商品"
        ]


        for word in replace_words:

            if word in message:

                message = message.replace(
                    word,
                    entity
                )


        return message



# 全局Memory

context_manager = ContextManager()