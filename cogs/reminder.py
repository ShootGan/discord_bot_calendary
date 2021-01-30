import os
from datetime import datetime

import pymongo
from discord.ext import commands

base_key = os.getenv('DBKEY')
my_db_name = os.getenv('DBNAME')
mycol_name = os.getenv('DBCOL')
client = pymongo.MongoClient(base_key)
mydb = client[my_db_name]
mycol = mydb[mycol_name]


def add_new_sesion(data):
    groups = {'G1': 'Gracze I', 'G2': 'Gracze II', 'G3': 'Gracze III', 'G4': 'Gracze IV'}

    data = data.split()
    if len(data) == 4:

        try:
            group = groups[data[1]]
        except Exception as err:
            print(err)
            return ('Ale takiej grupy nie ma byq')
        try:
            date = data[2] + ' ' + data[3] + ':00'
            date = datetime.strptime(date, '%d/%m/%y %H:%M:%S')

        except Exception as err:
            print(err)
            return ('źle podałeś date albo godzinę byq')
    else:
        return ('Źle coś wpisałeś')
    data_col = {
        "name": data[0],
        "group": group,
        "date": date,
        "remebers": 0,
    }
    try:
        x = mycol.insert_one(data_col)
        print(x.inserted_id)
    except Exception as err:
        print(err)
        return ('Błąd bazy danych')
    return ('Sesja dodana! :D')


class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client

    ##Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')

    ##Commands
    @commands.command()
    async def sesja(self, ctx, *, sesja_parm):
        print(sesja_parm)
        response = (add_new_sesion(sesja_parm))
        await ctx.send(response)


def setup(client):
    client.add_cog(Reminder(client))
