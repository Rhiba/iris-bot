import asyncio
import datetime
import os
from collections.abc import Iterable

import discord
import json

from creds import CREDS
from models import db_session, User, Reminder
from utils.command import process_commands
from utils.gym import check_for_classes
from utils.karma import karma_parse, karma_change
from utils.responses import FileResponse

token = CREDS['DISCORD_TOKEN']

client = discord.Client()

async def gym_check():
    await client.wait_until_ready()
    exercise_channel_id = 600743628356190214
    channel = client.get_channel(exercise_channel_id)
    while not client.is_closed():
        response = check_for_classes() 
        if not response == '':
            await channel.send(response)
        await asyncio.sleep(60)

async def reminder_check():
    await client.wait_until_ready()
    while not client.is_closed():
        # first get all the none "done" reminders
        not_done = db_session.query(Reminder).filter(Reminder.done == False).all()
        for nd in not_done:
            # if trigger time is in the past
            if nd.trigger_time < datetime.datetime.utcnow():
                content = nd.content
                rid = nd.id
                # set done to True
                nd.done = True
                db_session.commit()

                user_id = nd.user_id
                user = db_session.query(User).filter(User.id == user_id).first()
                channel = client.get_channel(nd.channel_id)
                response = f'<@!{user.uid}> {content}'
                await channel.send(response)
        # TODO: make this granularity set-able
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # bot should not respond to itself
    if message.author == client.user:
        return

    author = message.author.id
    user = db_session.query(User).filter(User.uid == author).first()
    if not user:
        new_user = User(uid=author,admin=0)
        db_session.add(new_user)
        db_session.commit()

    # if message is a command, we want to do something with it
    first_word = message.content.split()[0].lower()
    bot_username = client.user.name.lower()
    if (first_word in {"iris", f"<@!{client.user.id}>", bot_username}
            or (first_word.startswith('!')
                and first_word != "!"
                and first_word[1] not in '! ')):
        reply = process_commands(db_session, client, message)
        if isinstance(reply, FileResponse):
            await message.channel.send(reply.content, file=reply.file)
        elif isinstance(reply, str) and reply:
            await message.channel.send(reply)
        elif isinstance(reply, list):
            for r in map(str, reply):
                if r:
                    await message.channel.send(r)
    # otherwise, it might contain karma so we should parse it for karma
    else:
        changes = karma_parse(message)
        if len(changes) > 0:
            reply = karma_change(db_session, client, author, changes)
            await message.channel.send(reply)

client.loop.create_task(gym_check())
client.loop.create_task(reminder_check())
client.run(token)
