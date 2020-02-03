import os
import discord
import json

with open('creds.json') as cf:
    credentials = json.load(cf)

token = credentials['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # bot should not respond to itself
    if message.author == client.user:
        return

    if message.content.lower().startswith('iris ') or message.content.startswith('!') or message.content.startswith(f'<@{client.user.id}> '):
        await message.channel.send('All I can do is say hello for now: Hello!')

client.run(token)
