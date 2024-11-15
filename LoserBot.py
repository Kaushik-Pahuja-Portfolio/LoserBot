import discord
from discord.ext import commands
import re
import requests
import os
import random
from google.cloud import secretmanager
import signal

# APIKEY = os.environ.get("DISCORD_TOKEN")

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
        cards = re.findall(r'\[\[[a-zA-Z0-9\'\",.?!\s]+\]\]', message.content)
        cards = list(map(lambda c: {"name" : c[2:-1]}, cards))
        if len(cards) > 0:
            res = requests.request("POST", "https://api.scryfall.com/cards/collection", json={
                "identifiers": cards
            })
            data = res.json()
            if 'data' in data.keys() and len(data['data']) > 0:
                msg = []
                # msg = "\n".join(list(map(lambda c: c['image_uris']['png'], data['data'])))
                for c in data['data']:
                    if 'image_uris' in c.keys():
                        msg.append(c['image_uris']['png'])
                    else:
                        for f in c['card_faces']:
                            msg.append(f['image_uris']['png'])
                for i in range(0, len(msg), 5):
                    await message.channel.send("\n".join(msg[i:i+5]))
        await(client.process_commands(message))


@client.command()
async def test(ctx):
    usr = await client.fetch_user(ctx.author.id)
    await ctx.send(f"if you're reading this it worked {usr.mention}",silent=True)
    pass

@client.command()
async def mtg(ctx, arg):
    pass

@client.command()
async def roll(ctx, *args):
    arg = " ".join(args)
    rolls = re.findall(r"([0-9]+)d([0-9]+)([+-/*]?)([0-9]+)?", arg)
    #print(arg, rolls)
    lines = []
    sums = []
    for roll in rolls:
        s = "("
        results = []
        for i in range(int(roll[0])):
            results.append(random.randint(1, int(roll[1])))
        s += " + ".join(str(x) for x in results) + ")"
        if roll[2] != '':
            s += " " + " ".join(roll[2:])
        total = eval(s)
        sums.append(int(total))
        s = f"{roll[0]}d{roll[1]}{roll[2]}{roll[3]}: {s} = {int(total)}"
        if total != int(total): s += " (rounded down)"
        lines.append(s.replace("*", "\\*"))
    lines.append(f"total: {sum(sums)}")
    await ctx.send('\n'.join(lines))

@client.command()
async def die(ctx, arg = "pls"):
    quit()

#main runner
secretClient = secretmanager.SecretManagerServiceClient()
client.run(secretClient.access_secret_version(request={"name": "projects/116342818934/secrets/bot_token/versions/latest"}).payload.data.decode("UTF-8"))
