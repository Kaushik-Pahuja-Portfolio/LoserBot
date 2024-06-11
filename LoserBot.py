import discord
from discord.ext import commands
import re
import requests
import os

intents = discord.Intents.default()
intents.message_content=True
client = commands.Bot(command_prefix='!',help_command=None,intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    #doesnt read the messages from bot
    if message.author == client.user:
        return
    else: 
        cards = re.findall('~\[[a-zA-Z0-9\s\'\",.?!]+\]', message.content)
        cards = list(map(lambda c: {"name" : c[2:-1]}, cards))
        if len(cards) > 0:
            res = requests.request("POST", "https://api.scryfall.com/cards/collection", json={
                "identifiers": cards
            })
            data = res.json()
            if 'data' in data.keys() and len(data['data']) > 0:
                msg = "\n".join(list(map(lambda c: c['image_uris']['png'], data['data'])))
                await message.channel.send(msg)
        await(client.process_commands(message))

@client.command()
async def test(ctx):
    await ctx.send("hello @everyone",silent=True)
    pass

@client.command()
async def mtg(ctx, arg):
    pass
print(os.environ)
#main runner
client.run(os.getenv("DISCORD_TOKEN"))