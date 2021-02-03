import os
from datetime import datetime, timedelta

import discord
import pymongo
from discord.ext import commands, tasks
from discord.utils import get

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

    def __init__(self, bot):
        self.bot = bot



    ##Events
    @commands.Cog.listener()
    async def on_ready(self):
        self.send_notification.start()
        print('bot is ready')


        # tasks
    @tasks.loop(minutes=1)
    async def send_notification(self):
        channel = self.bot.get_channel(704695378838290462)
        minusdate = datetime.now() + timedelta(days=1)
        mention = {'Gracze I': '<@&806275258725957702>', 'Gracze II': '<@&806275316682063943>',
                   'Gracze III': '<@&806275354783383574>', 'Gracze IV': '<@&806275451676655666>'}
        for x in mycol.find({'date': {"$lt": minusdate}}):

            if x['date'] < (datetime.now() + timedelta(days=1)) and x['remebers'] == 0:

                await channel.send(mention[x['group']]+" Jutro sesja")
                mycol.update_one({'_id': x['_id']}, {"$set": {"remebers": 1}})
            elif x['date'] < (datetime.now() + timedelta(minutes=30)) and x['remebers'] == 1:

                await channel.send(mention[x['group']]+ " 30 minut do grania")
                mycol.update_one({'_id': x['_id']}, {"$set": {"remebers": 2}})
            elif x['date'] < datetime.now() and x['remebers'] == 2:

                await channel.send(mention[x['group']] + " Sesjaaaaa!")
                mycol.delete_one({"_id": x['_id']})

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
