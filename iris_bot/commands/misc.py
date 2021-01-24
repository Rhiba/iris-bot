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


def contract(db_session, message, *args):
    if len(args) == 1:
        reply = args[0][0]
        reply += str(len(args[0][1:-1]))
        reply += args[0][-1]
        return [reply]
    else:
        return ['Exactly one item please.']


def timer(db_session, message, *args):
    return ['Not implemented.']
