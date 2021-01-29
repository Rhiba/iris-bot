import random
import yaml

__all__ = ["poem", "printpoems", "addpoem"]


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
