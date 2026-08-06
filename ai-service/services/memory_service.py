import copy

memory={
    "last_result": None,
    "last_entity": None,
    "last_intent": None,
    "last_sql": None,
    "last_table": None
}

def save_context( 
        data=None,
        intent=None,
        sql=None,
        table=None):


    if intent:
        memory["last_intent"] = intent

    if sql:
        memory["last_sql"] = sql

    if table:
        memory["last_table"] = table

    if data:
        memory["last_result"] = data

        if isinstance(data, list) and len(data) > 0:


          first = data[0]


          # 商品
          if "item_name" in first:
            memory["last_entity"] = first["item_name"]


          # 品牌
          elif "brand" in first:
            memory["last_entity"] = first["brand"]



    




def get_context():

    return copy.deepcopy(memory)




def resolve_context(message):

    entity = memory.get("last_entity")

    if not entity:
        return message


    words = [
        "它",
        "这个商品",
        "这个",
        "那个"
    ]

    for word in words:

        if word in message:
            message = message.replace(
                word,
                entity
            )

    return message