import os
import discord
import json
from utils.karma import karma_parse, karma_change
from creds import CREDS
from models import db_session, User

token = CREDS['DISCORD_TOKEN']

client = discord.Client()

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
    if message.content.lower().startswith('iris ') or message.content.startswith('!') or message.content.startswith(f'<@{client.user.id}> '):
        await message.channel.send('All I can do is say hello for now: Hello!')
    # otherwise, it might contain karma so we should parse it for karma
    else:
        changes = karma_parse(message)
        if len(changes) > 0:
            reply = karma_change(db_session, author, changes)
            await message.channel.send(reply)


client.run(token)
