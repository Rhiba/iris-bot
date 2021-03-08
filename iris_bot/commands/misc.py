__all__ = ["gym_notify", "say", "widen", "contract", "timer"]

def gym_notify(db_session, message, *args):
    if not len(args) == 2:
        print('Wrong number of arguments.')
    class_name = args[0]
    class_time = args[1]
    return ['test']


def say(db_session, message, *args):
    if len(args) == 0:
        return ['say wot mate?']
    return [' '.join(args)]


def widen(db_session, message, *args):
    if len(args) > 0:
        reply = ""
        for a in args:
            for c in a.upper():
                reply += c + " "
        return [reply]
    else:
        return ['No item provided.']


def contract(db_session, message, *input_words):
    contractions = []
    for word in input_words:
        try:
            first, *middle, last = filter(str.isalpha, word)
        except ValueError:
            continue
        contractions.append(f"{first}{len(middle)}{last}")
    if contractions:
        return [" ".join(contractions)]
    return ["No valid words to contract."]


def timer(db_session, message, *args):
    return ['Not implemented.']
