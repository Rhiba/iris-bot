from models import Karma, KarmaChange, GymNotification, GymToken
from sqlalchemy import desc
import random

def gym_notify(db_session, *args):
    if not len(args) == 2: 
        print('Wrong number of arguments.')
    class_name = args[0]
    class_time = args[1]
    return ['test']

def say(db_session, *args):
    return [' '.join(args)]

def flip(db_session, *args):
    if len(args) == 0:
        return ["🖕"]
    result = random.randint(0, len(args)-1)
    return [args[result]]

def roll(db_session, *args):
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

def karma(db_session, *args):
    reply = ''
    if len(args) == 0:
        return ['No item provided.']

    items = []
    no_karma = []
    for a in args:
        a = a.strip().lower()
        kitem = db_session.query(Karma).filter(Karma.name == a).one_or_none()
        if kitem:
            last_change = db_session.query(KarmaChange).filter(KarmaChange.karma_id==kitem.id).order_by(desc(KarmaChange.changed_at)).first()
            items.append((a,last_change.score))
        else:
            no_karma.append(a)

    if len(items) > 1:
        k_plural = 's are'
    else:
        k_plural = ' is'

    if len(no_karma) > 1:
        nk_plural = 'these have'
    else:
        nk_plural = 'this has'


    if len(items) > 0:
        reply += f'The karma score{k_plural} as follows:\n'
        for i,s in items:
            reply += f' • **{i}** ({s})\n'

    if len(no_karma) > 0:
        reply += f'Sorry, {nk_plural} no karma:\n'
        for nk in no_karma:
            reply += f' • **{nk}**\n'

    return [reply.rstrip()]
