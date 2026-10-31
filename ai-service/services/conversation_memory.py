"""对话历史：只留最近两轮。

历史越长，每次回答带的输入越多。指代问题靠 Redis 里的实体解决，
聊天历史只负责让普通对话不突兀，四条目就够。
"""

MAX_HISTORY = 4

_history = []


def add_message(role, content):

    _history.append({"role": role, "content": content})

    if len(_history) > MAX_HISTORY:

        del _history[:-MAX_HISTORY]


def get_history():

    return list(_history)


def clear():

    _history.clear()
