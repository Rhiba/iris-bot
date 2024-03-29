from collections.abc import Iterable
from models import Command, User
import commands
from inspect import getmembers, isfunction
import re

functions_list = [o for o in getmembers(commands) if isfunction(o[1])]
function_names = [o[0] for o in functions_list]


def is_non_str_iterable(x):
    return isinstance(x, Iterable) and not isinstance(x, str)


def truncate_message(msg, length=2000):
    """ Limit message length and add truncation notice """
    if not isinstance(msg, str):
        return msg
    truncation_message = " *<truncated due to length>*"
    MAX_LEN = 2000
    if len(msg) > MAX_LEN:
        truncation_point = MAX_LEN - len(truncation_message)
        return msg[:truncation_point] + truncation_message
    return msg


def process_commands(db_session,  client, message):
    user = db_session.query(User).filter(User.uid == message.author.id).first()
    # here we want to split the commands up by pipes
    # we also want to pull commands from the hard coded ones, or the composite commands in the Command table (that are user defined)
    if message.content.startswith('!'):
        content = message.content[1:]
    else:
        content = ' '.join(message.content.split(' ')[1:])

    # for now, if command starts with !s/ IGNORE IT
    if content.split(' ')[0].lower().startswith('s/'):
        return ""
    # different case for alias command
    if content.split(' ')[0].lower() == 'alias':
        command_name = content.split(' ')[1].lower()
        if command_name == 'alias':
            return "Command already exists: alias."
        else:
            exist_command = db_session.query(Command).filter(Command.name == command_name).one_or_none()
            if exist_command:
                return f"Command already exists: {command_name}."
        command_string = ' '.join(content.split(' ')[2:])
        if 'alias' in command_string:
            return "Can't use alias command inside alias command."
        else:
            new_command = Command(user_id=user.id,name=command_name,description='',command_string=command_string)
            db_session.add(new_command)
            db_session.commit()
            return f"Added command: {command_name}."


    commands = content.split('|')
    commands = [c.strip() for c in commands]
    # iterate through commands until all of them have been transformed down to their hard coded version
    idx = 0
    depth = 0
    while idx < len(commands):
        depth += 1
        if depth == 1001:
            return 'Max loop depth reached (what did you do?!).'
        command = commands.pop(idx).strip()
        # get first word
        words = command.split(' ')
        initial = words[0].lower()
        rest = None
        if len(words) > 1:
            rest = words[1:]

        if initial in function_names:
            commands.insert(idx,command)
            idx += 1
        else:
            db_entry = db_session.query(Command).filter(Command.name == initial).one_or_none()
            if db_entry is None:
                if initial == 'alias':
                    return 'Alias can only be used as a standalone command.'

                bot_username = client.user.name.lower()
                mg = message.content.lower()
                if mg.startswith('iris ') or mg.startswith(f"<@!{client.user.id}> ") or mg.startswith(bot_username+' '):
                    return ''
                return f'Command not found: {initial}'

            command_string = db_entry.command_string
            new_command = command_string
            highest = 0
            if len(new_command.split(' ')) > 1:
                tail_command = new_command.split(' ')[1:]
                for a in tail_command:
                    m = re.match('<([0-9]+)>',a)
                    if m:
                        num = int(m.group(1))
                        if num > highest:
                            highest = num

                if highest > 0:
                    for i in range(highest):
                        if rest and len(rest) > 0:
                            current = rest.pop(0)
                            indices = [idx for idx,x in enumerate(tail_command) if x == '<'+str(i+1)+'>']
                            for ind in indices:
                                tail_command[ind] = current
                        elif rest:
                            return f'Not enough arguments supplied'

            new_command = new_command.split(' ')[0] + ' ' + ' '.join(tail_command)

            if not rest == None:
                new_command += ' ' + ' '.join(rest)

            new_commands = new_command.split('|')
            commands = commands[:idx] + new_commands + commands[idx:]

    # input placeholders given by <1> <2> etc, if none given, assume output of previous command goes to final input(s) of next command
    outputs = []
    for command in commands:
        command_name = command.split(' ')[0]
        func = [o[1] for o in functions_list if o[0] == command_name][0]
        args = command.split(' ')[1:]
        args = [a.strip() for a in args]

        # get highest placeholder num in args

        for idx, o in enumerate(outputs):
            if is_non_str_iterable(o):
                o = "\n".join(o)

            pos_string = f'<{idx+1}>'
            if pos_string not in args:
                args.extend(o.split())
            else:
                indices = [idx for idx, x in enumerate(args) if x == pos_string]
                for ind in indices:
                    args = args[:ind] + o.split() + args[ind+1:]
        reply = func(db_session, message, *args)
        outputs.extend(reply)

    output_message = outputs[-1]
    if is_non_str_iterable(output_message):
        output_message = [truncate_message(m) for m in output_message]
    else:
        output_message = truncate_message(output_message)
    return output_message
