import dateutil
import random
import re
from itertools import starmap

from sqlalchemy import desc

import utils.e4d
from models import Karma, KarmaChange, GymNotification, GymToken, Reminder, User
from utils.quotes import quotes
import yaml
import utils.randomperks
    
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
            first, *middle, last = word
        except ValueError:
            continue
        contractions.append(f"{first}{len(middle)}{last}")
    if contractions:
        return [" ".join(contractions)]
    return ["No valid words to contract."]


def karma(db_session, message, *args):
    reply = ''
    if len(args) == 0:
        return ['!karma <item>']

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

def remindme(db_session, message, *args):
    reply = ''
    if len(args) == 0:
        # TODO: make this granularity set-able
        return ['!remindme <date/time> <message>\nFormat (brackets optional, either date, time or both):\n** - (dd/mm(/yy(yy))) (hh:mm(:ss))**\nGranularity set to 10s.']
    elif len(args) == 1:
        return ['Missing argument.']
    else:
        date = None
        time = None
        if re.match(r'^[0-3]?[0-9]/[01]?[0-9](/[0-9][0-9]([0-9][0-9])?)?$',args[0]):
            # got a date
            date = args[0]
        i = 0 if date == None else 1

        if re.match(r'[0-2]?[0-9]:[0-5]?[0-9](:[0-5]?[0-9])?',args[i]):
            time = args[i]

        if time == None and date == None:
            return ['Invalid time and date format.']

        date_str = ''
        if not date == None:
            date_str += date + ' '
        if not time == None:
            date_str += time
        date_str = date_str.strip()

        valid_date = None
        try:
            valid_date = dateutil.parser.parse(date_str,dayfirst=True)
        except ValueError:
            return ['Date doesn\'t exist.']

        if time == None or date == None:
            content = ' '.join(args[1:])
        else:
            content = ' '.join(args[2:])

        user = db_session.query(User).filter(User.uid == message.author.id).first()
        channel_id = message.channel.id
        trigger_time = valid_date
        # used to constantly message a person about it until they say otherwise
        persistent = False

        reminder = Reminder(
            user_id = user.id,
            channel_id = channel_id,
            trigger_time = trigger_time,
            content = content,
            persistent = persistent
        )
        db_session.add(reminder)
        db_session.commit()
        return ['Added reminder on ' + str(valid_date) + '.']

def timer(db_session, message, *args):
    return ['Not implemented.']

def uplift(db_session, message, *args):
    x = random.choice(quotes)
    return [x]

def poem(db_session, message, *args):
    with open('data/poems.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader) 
    #if no argument given, post a random poem
    if len(args) == 0: 
        poems_list = list(data.items())
        poet, poems = random.choice(poems_list)
        poem_name, poem = random.choice(list(poems.items()))
        return [poem_name + " by " + poet.title() + "\n\n" + poem]
    #if an author is specified, post a random poem by that poet
    author = " ".join(args).lower()
    if author in data:  
        poems = data[author] 
        poem_name, poem = random.choice(list(poems.items()))
        return [poem_name + "\n\n" + poem]
    if author not in data:
        return ["Sorry, I don't have any poems by that author. Why not add a poem using !addpoem?"]

def printpoems(db_session, message, *args):
    with open('data/poems.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader) 
    #Post all poems by the specified author
    author = " ".join(args).lower()
    for author in data: 
        poems = data[author]
        poems_list = list(poems)
        return ["Poems by " + author + " include: \n" + str(poems_list)]

def addpoem(db_session, message, *args):
    with open('data/poems.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader) 
    author, title, poem = " ".join(args).split(',', maxsplit=2)
    poem = poem.strip()
    #if author is already there
    if author in data:
        data[author][title] = poem
    #if author is not already there, create a new entry 
    else:
        data[author] = {title : poem}
    with open('data/poems.yaml', 'w') as f:
        yaml.dump(data, f)
    return ['I have added your poem to my database']
    



def e4d(db_session, message, *input_words):
    if utils.e4d.SYSTEM_WORDS_LIST is None:
        return ["<e4d disabled>"]
    if not input_words:
        return ["Example usage:\n\t!e4d i18n\n\t!e4d i18n a11y"]

    return [" ".join([
        random.choice(matches)
        for matches in utils.e4d.get_matches(input_words)
        if matches
    ])]


def e5d(db_session, message, *input_words):
    if utils.e4d.SYSTEM_WORDS_LIST is None:
        return ["<e5d disabled>"]
    if not input_words:
        return ["Example usage:\n\t!e5d i18n\n\t!e5d i18n a11y"]

    matches = utils.e4d.get_matches(input_words)
    output_lines = starmap(utils.e4d.to_output_line, zip(input_words, matches))
    return utils.e4d.to_output_messages(output_lines)

def randomperks(db_sesson, message, *args):
    try:
        if not args:
             raise Exception("Use !randomperks killer or !randomperks survivor")
        else:
            return utils.randomperks.get_perks(args[0])
    except Exception as e:
        print("exception")
        return [str(e)]
