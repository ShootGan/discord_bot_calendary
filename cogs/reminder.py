import discord
import pandas as pd
from discord.ext import commands
from token_r import read_token


def create_table():
    kolumnny = ['nazwa', 'grupa', 'data', 'godzina']
    data_table = pd.DataFrame(columns=kolumnny)
    return data_table


Data_table = create_table()
print(Data_table)
def add_new_sesion(wejscie):
    wejscie = wejscie.split()
    x=1
    print(wejscie)
    return x

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

        print(sesja_parm)
        print(add_new_sesion(sesja_parm))

def setup(client):
    client.add_cog(Reminder(client))
