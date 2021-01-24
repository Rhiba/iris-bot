import random

__all__ = ["flip", "roll"]


def flip(db_session, message, *args):
    if len(args) == 0:
        return ["🖕"]
    result = random.randint(0, len(args)-1)
    return [args[result]]


def roll(db_session, message, *args):
    if len(args) != 1 and len(args) != 2:
        return ['!roll <x>d<y> <opt> - roll a y sided die x times (optionally take the high or sum)']
    pos = args[0].find('d')
    if pos == -1:
        return ['!roll <x>d<y> <opt> - roll a y sided die x times (optionally take the high or sum)']

    if random.randint(0, 100) == 0:
        return ['NUMBERWANG']

    s = 0
    h = 0
    result = ''

    try:
        for dice in range(int(args[0][:pos])):
            if result != '':
                result += ', '
            outcome = random.randint(1, int(args[0][pos+1:]))
            if h < outcome:
                h = outcome
            s += outcome
            result += str(outcome)
    except ValueError:
        return ["Please give me integers!"]

    if len(args) == 2 and args[1] == 'high':
        result += f" (high={h})"
    elif len(args) == 2 and args[1] == 'sum':
        result += f" (sum={s})"

    return [result]
