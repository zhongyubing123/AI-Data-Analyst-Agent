import copy
import json

from services.redis_client import get_redis


MEMORY_KEY = "agent:memory:default"

MEMORY_EXPIRE = 24 * 60 * 60


def get_memory():

    redis = get_redis()

    data = redis.get(MEMORY_KEY)


    if data:

        return json.loads(data)


    return {
        "last_result": None,
        "last_entity": None,
        "last_intent": None,
        "last_sql": None,
        "last_table": None,
        "last_entity_type": None
    }



def save_context(
        data=None,
        intent=None,
        sql=None,
        table=None
):

    memory = get_memory()



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


            if "item_name" in first:

                memory["last_entity"] = (
                    first["item_name"]
                )

                memory["last_entity_type"] = "item"



            elif "brand" in first:

                memory["last_entity"] = (
                    first["brand"]
                )

                memory["last_entity_type"] = "brand"



            elif "category_name" in first:

                memory["last_entity"] = (
                    first["category_name"]
                )

                memory["last_entity_type"] = "category"



    redis = get_redis()


    redis.set(
        MEMORY_KEY,
        json.dumps(
            memory,
            ensure_ascii=False
        ),
        ex=MEMORY_EXPIRE
    )



def get_context():

    return copy.deepcopy(
        get_memory()
    )

def get_sql_context():

    memory = get_memory()


    return {

        "last_entity":
        memory.get("last_entity"),


        "last_entity_type":
        memory.get("last_entity_type"),


        "last_table":
        memory.get("last_table")

    }

def resolve_context(message):

    memory = get_memory()


    entity = memory.get(
        "last_entity"
    )


    if not entity:

        return message



    replace_words = [

        "它",

        "这个商品",

        "这个",

        "那个"

    ]



    for word in replace_words:


        if word in message:


            message = message.replace(
                word,
                entity
            )


    return message