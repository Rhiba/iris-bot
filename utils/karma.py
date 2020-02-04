import os
import discord
import re
from models import User, Karma, KarmaChange
from sqlalchemy import desc
from datetime import datetime, timedelta

from creds import CREDS

def karma_parse(message):
    karma_regex = re.compile(r'(((("|\')(.*)(\4)|([^ \n]*))(\+\+|\+\-|\-\+|\-\-)( )?)+)(\(.*\)|(because|for)([^;\n]*?(?=( (("|\').*(\15)|[^ \n]*)(\+\+|\+\-|\-\+|\-\-))|[;\n]|$)))?')
    re_iter = karma_regex.finditer(message.content)
    karma_changes = []
    for r in re_iter:
        g = r.groups()
        items = []
        quote_stack = []
        current_item = ''
        idx = 0
        while idx < len(g[0]):
            ch = g[0][idx]
            if ch == '"' and len(quote_stack) > 0 and quote_stack[-1] == '"':
                quote_stack.pop()
                current_item += g[0][idx+1] + g[0][idx+2]
                items.append(current_item)
                current_item = ''
                idx += 4
            elif ch == "'" and len(quote_stack) > 0 and quote_stack[-1] == "'":
                quote_stack.pop()
                current_item += g[0][idx+1] + g[0][idx+2]
                items.append(current_item)
                current_item = ''
                idx += 4
            elif ch == "'" or ch == '"':
                quote_stack.append(ch)
                idx += 1
            elif ch == '+' or ch == '-' and len(quote_stack) == 0:
                current_item += ch + g[0][idx+1]
                items.append(current_item)
                current_item = ''
                idx += 3
            else:
                current_item += ch
                idx += 1

        reason = g[9].strip() if g[9] else g[9]
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

def karma_change(db_session, uid, changes):
    # get user from db
    user = db_session.query(User).filter(User.uid == uid).first()

    changed = []
    not_changed = []

    for tup in changes:
        karma_name = tup[0].lower()
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
                changed.append((tup[0],karma_change.score))
            else:
                not_changed.append(tup[0])
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
            changed.append((tup[0],karma_change.score))

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
        for c,s in changed:
            reply += f" • **{c}** (new score is {s})\n"

    if len(not_changed) > 0:
        reply += f"Unfortunately, I couldn't make changes to the following item{n_item_plural} because of the cooldown period:\n"

        for c in not_changed:
            reply += f" • **{c}**\n"

    return reply.rstrip()


