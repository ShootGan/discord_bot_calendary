import os
from datetime import datetime

import discord
import pymongo
from discord.ext import commands

base_key = os.getenv('DBKEY')
my_db_name = os.getenv('DBNAME')
mycol_name = os.getenv('DBCOL')
client = pymongo.MongoClient(base_key)
mydb = client[my_db_name]
mycol = mydb[mycol_name]


##Add new sesion
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


# Show all sesions
def show_all_sesions():
    sesions_list = list(mycol.find({'date': {"$gt": datetime.now()}}, {'_id': 0, 'remebers': 0}).sort('date'))
    # sesions_list = Tomark.table(sesions_list)
    print(sesions_list)
    return sesions_list


# Find given sesions
def find_my_sesions(group):
    try:
        groups = {'G1': 'Gracze I', 'G2': 'Gracze II', 'G3': 'Gracze III', 'G4': 'Gracze IV'}
        group = groups[group]
    except Exception as err:
        print(err)
        return ('zła grupa')
    print(group)
    try:
        your_sesions_list = list(
            mycol.find({'date': {"$gt": datetime.now()}, "group": group}, {"_id": 0, 'remebers': 0}).sort('date'))

    except Exception as err:
        print(err)
        return ('nie masz żadnych sesji przegrywie')
    return your_sesions_list


class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client

    ##Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')

    ##Commands
    ##Make new sesion
    @commands.command()
    async def sesja(self, ctx, *, sesja_parm):
        print(sesja_parm)
        response = (add_new_sesion(sesja_parm))
        await ctx.send(response)

    ##Show all sesions
    @commands.command()
    async def sesje(self, ctx):
        response = (show_all_sesions())
        embed = discord.Embed(title="Wszystkie sesje:")
        for x in response:
            timeto = str(abs(x['date'] - datetime.now())).split(".")[0]

            print(timeto)
            embed.add_field(name=x['date'], value='**Nazwa:** ' + x['name'] + '\n' + '**Grupa:** ' + x[
                'group'] + '\n' + '**Za:** ' + timeto, inline=False)
        await ctx.send(embed=embed)

        ##Show all sesions

    @commands.command()
    async def moje(self, ctx, *, group):
        response = (find_my_sesions(group))
        embed = discord.Embed(title="Wybrane sesje:")
        for x in response:
            timeto = str(abs(x['date'] - datetime.now())).split(".")[0]

            print(timeto)
            embed.add_field(name=x['date'], value='**Nazwa:** ' + x['name'] + '\n' + '**Za:** ' + timeto, inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Reminder(client))
