import discord
from models import Command, User
import commands
from inspect import getmembers, isfunction

functions_list = [o for o in getmembers(commands) if isfunction(o[1])]
function_names = [o[0] for o in functions_list]

def process_commands(db_session, message):
    user = db_session.query(User).filter(User.uid == message.author.id).first()
    # here we want to split the commands up by pipes
    # we also want to pull commands from the hard coded ones, or the composite commands in the Command table (that are user defined)
    if message.content.startswith('!'):
        content = message.content[1:]
    else:
        content = ' '.join(message.content.split(' ')[1:])

    commands = content.split('|')
    # iterate through commands until all of them have been transformed down to their hard coded version
    idx = 0
    while idx < len(commands):
        command = commands.pop(idx)
        # get first word
        words = command.split(' ')
        initial = words[0]
        rest = None
        if len(words) > 1:
            rest = words[1:]

        if initial in function_names:
            commands.insert(idx,command)
            idx += 1
        else:
            db_entry = db_session.query(Command).filter(Command.name == initial).one_or_none()
            if db_entry == None:
                return f'Command not found: {initial}'

            command_string = db_entry.command_string
            new_command = command_string
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
        # check for placeholders here
        for a in args:
            #TODO
            pass
        reply = func(*args)
        outputs.append(reply)

    return outputs[-1]

