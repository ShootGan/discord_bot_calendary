import discord
from discord.ext import commands
from token_r import read_token

class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client
    ##Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')
    ##Commands
    @commands.command()
    async def sesja(self,ctx,*,sesja_parm):
        await ctx.send(sesja_parm)

def setup(client):
    client.add_cog(Reminder(client))
