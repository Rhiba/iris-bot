import os
import discord
import re
from models import User, Karma, KarmaChange
from sqlalchemy import desc
from datetime import datetime, timedelta

from creds import CREDS

def filter_codeblocks(content):
    filtering = False
    remove_indices = []
    start_index = -1
    end_index = -1
    for idx,ch in enumerate(content):
        if filtering == False and ch == '`' and content[idx+1] == '`' and content[idx+2] == '`':
            filtering = True
            start_index = idx
        elif filtering == True and ch == '`' and content[idx-1] == '`' and content[idx-2] == '`':
            filtering = False
            end_index = idx
            remove_indices.append((start_index,end_index))

    output = ''
    if len(remove_indices) == 0:
        output = content
    else:
        prev = 0
        for ri in remove_indices:
            output += content[prev:ri[0]]
            prev = ri[1]+1
        output += content[prev:]

    return output

def filter_inlinecode(content):
    filtering = False
    remove_indices = []
    start_index = -1
    end_index = -1
    for idx,ch in enumerate(content):
        if filtering == False and ch == '`':
            filtering = True
            start_index = idx
        elif filtering == True and ch == '`':
            filtering = False
            end_index = idx
            remove_indices.append((start_index,end_index))

    output = ''
    if len(remove_indices) == 0:
        output = content
    else:
        prev = 0
        for ri in remove_indices:
            output += content[prev:ri[0]]
            prev = ri[1]+1
        output += content[prev:]

    return output

def karma_parse(message):
    karma_regex = re.compile(r'(((("|\')(.+)(\4)|([^ \n]+))(\+\+|\+\-|\-\+|\-\-)( )?)+)(\(.*\)|(because|for)([^;\n]*?(?=( (("|\').+(\15)|[^ \n]+)(\+\+|\+\-|\-\+|\-\-))|[;\n]|$)))?')
    item_regex = re.compile(r'((("|\')(.+)(\3)|([^ \n]+))(\+\+|\+\-|\-\+|\-\-))')
    content = filter_codeblocks(filter_inlinecode(message.content))
    re_iter = karma_regex.finditer(content)
    karma_changes = []
    for r in re_iter:
        g = r.groups()
        item_string = g[0]
        reason = g[9].strip() if g[9] else g[9]

        items = []
        item_iter = item_regex.finditer(item_string)
        for it in item_iter:
            i = it.groups()[0]
            string_name = i[:-2]
            if len(string_name) >= 3 and string_name.startswith('"') and string_name.endswith('"'):
                items.append(string_name[1:-1] + i[-2:])
            elif len(string_name) >= 3 and string_name.startswith("'") and string_name.endswith("'"):
                items.append(string_name[1:-1] + i[-2:])
            elif len(string_name) > 1:
                items.append(i)

        for item in items:
            name = item[:-2]
            suffix = item[-2:]
            if suffix == '++':
                change = 1
            elif suffix == '+-' or suffix == '-+':
                change = 0
            else:
                change = -1
            karma_changes.append((name,change,reason))

    return karma_changes

def karma_change(db_session, client, uid, changes):
    # get user from db
    user = db_session.query(User).filter(User.uid == uid).first()

    changed = []
    not_changed = []

    for tup in changes:
        karma_name_raw = tup[0]
        karma_name = tup[0].lower()
        if karma_name == 'me':
            d_user = client.get_user(uid)
            karma_name_raw = d_user.name
            karma_name = d_user.name.lower()
        change = tup[1]
        reason = tup[2]
        # first, check if the karma_name already exists in karma database
        karma_item = db_session.query(Karma).filter(Karma.name == karma_name).one_or_none()
        if karma_item == None:
            # add it to the karma table
            karma_item = Karma(name=karma_name)
            db_session.add(karma_item)
            db_session.commit()

        # check when last altered
        last_change = db_session.query(KarmaChange).filter(KarmaChange.karma_id == karma_item.id).order_by(desc(KarmaChange.changed_at)).first()

        if last_change:
            time_delta = datetime.utcnow() - last_change.changed_at
            if time_delta >= timedelta(seconds=CREDS['KARMA_TIMEOUT_S']):
                # enough time has passed
                karma_change = KarmaChange(
                    karma_id=karma_item.id,
                    user_id=user.id,
                    reason=reason,
                    change=change,
                    score=last_change.score+change,
                    changed_at=datetime.utcnow()
                )
                db_session.add(karma_change)
                db_session.commit()
                changed.append((karma_name_raw,last_change.score,karma_change.score))
            else:
                not_changed.append(karma_name_raw)
        else:
            karma_change = KarmaChange(
                karma_id=karma_item.id,
                user_id=user.id,
                reason=reason,
                change=change,
                score=change,
                changed_at=datetime.utcnow()
            )
            db_session.add(karma_change)
            db_session.commit()
            changed.append((karma_name_raw,'None',karma_change.score))

        if change == -1:
            karma_item.pluses = karma_item.pluses + 1
        elif change == 0:
            karma_item.neutrals = karma_item.neutrals + 1
        else:
            karma_item.minuses = karma_item.minuses + 1

        db_session.commit()

    if len(changed) > 1:
        ch_item_plural = 's'
    else:
        ch_item_plural = ''

    if len(not_changed) > 1:
        n_item_plural = 's'
    else:
        n_item_plural = ''
    
    reply = ""
    if len(changed) > 0:
        reply += f"I have made changes to the following item{ch_item_plural}:\n"
        for c,o,s in changed:
            reply += f" • **{c}** ({o} -> {s})\n"

    if len(not_changed) > 0:
        reply += f"Unfortunately, I couldn't make changes to the following item{n_item_plural} because of the cooldown period:\n"

        for c in not_changed:
            reply += f" • **{c}**\n"

    return reply.rstrip()


