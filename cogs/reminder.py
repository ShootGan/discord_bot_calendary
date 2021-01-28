import discord
from discord.ext import commands
from token_r import read_token

class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')

    @comands.comand(name='planowanie sesji',help=' Po komendziej podaj: nazwa grupa data godzina')
        def async sesja(self,ctx,*,sesja_parm )
            await ctx.send(x)

def setup(client):
    client.add_cog(Reminder(client))
