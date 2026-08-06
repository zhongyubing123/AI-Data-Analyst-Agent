


conversation_history = []

MAX_HISTORY = 10



def add_message(role, content):

    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )


    if len(conversation_history) > MAX_HISTORY:

        del conversation_history[:-MAX_HISTORY]




def get_history():

    return conversation_history