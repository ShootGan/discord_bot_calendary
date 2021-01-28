import discord
from discord.ext import commands
from token_r import read_token
client = commands.Bot(command_prefix='!')

TOKEN= read_token()
if __name__ == '__main__':
    @client.event  ## start
    async def on_ready():
        print('bot is ready.')


    @client.command()  ##wpisanie danych
    async def sesja(ctx,*,x):
        await ctx.send(x)
    client.run(TOKEN)
