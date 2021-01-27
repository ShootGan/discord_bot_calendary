import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event  ## start
async def on_ready():
    print('bot is ready.')

def read_token():
    with open("token.txt",'r') as f:
        lines= f.readlines()
        return lines[0].strip()
TOKEN= read_token()
client.run(TOKEN)

