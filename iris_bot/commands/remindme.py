import dateutil
import re
from ..models import Reminder, User


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
