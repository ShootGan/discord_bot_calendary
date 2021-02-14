import os
from datetime import datetime, timedelta

import discord
import pymongo
from discord.ext import commands, tasks
import random
import discord.utils

import time

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

    except Exception as err:
        print(err)
        return ('Błąd bazy danych')
    return ('Sesja dodana! :D')


# Show all sesions
def show_all_sesions():
    sesions_list = list(mycol.find({'date': {"$gt": datetime.now()}}, {'_id': 0, 'remebers': 0}).sort('date'))
    # sesions_list = Tomark.table(sesions_list)

    return sesions_list


# Find given sesions
def find_my_sesions(group):
    try:
        groups = {'G1': 'Gracze I', 'G2': 'Gracze II', 'G3': 'Gracze III', 'G4': 'Gracze IV'}
        group = groups[group]
    except Exception as err:
        print(err)
        return ('zła grupa')

    try:
        your_sesions_list = list(
            mycol.find({'date': {"$gt": datetime.now()}, "group": group}, {"_id": 0, 'remebers': 0}).sort('date'))

    except Exception as err:
        print(err)
        return ('nie masz żadnych sesji przegrywie')
    return your_sesions_list


# dice
def dice(x):
    try:
        y = x
        y = y.split("d")
        rzuty = y[0]
        ilosc = y[1]
        wynik = []
        suma = 0
        for z in range(int(rzuty)):
            wynik.append(random.randint(1, int(ilosc)))
            suma = suma + wynik[z]
        return wynik, suma
    except:
        return ("coś źle wpisałeś mordeczko ;)"), ':(('


def gawena(content):
    jesienna = ['jesiennej', 'jesienna', 'jesieną', 'jesienną']
    gawenda = ['gawenda', 'gawende', 'gawendy', 'gawęda', 'gawendy', 'gawędę', 'gawęde', 'gawęde?', 'gawędę?']
    lubie = ['lubie', 'lubię', 'uwielbiam', 'kocham', 'jestem', 'fanem', 'pasja', 'pograć', 'pograł', 'pograli',
             'fajna', 'kox', 'super', 'lubuje', 'luba', 'kochulma', 'koham', 'chciałbym ruchać', 'chcialbym ruchać',
             'kochać', "uprawiać", 'seks', 'pyte']
    if any(jesien in content for jesien in jesienna):
        if any(gawend in content for gawend in gawenda):
            if any(like in content for like in lubie):
                return 1
    else:
        return 0


def delete_session(data):
    data = data.split()

    try:
        date = data[1] + ' ' + data[2] + ':00'
        date = datetime.strptime(date, '%d/%m/%y %H:%M:%S')

    except Exception as err:
        print(err)
        return ('źle podałeś date albo godzinę byq')

    delete_this = mycol.find_one({'date': date, 'name': data[0]}, {'remebers': 0})
    mycol.delete_one({"_id": delete_this['_id']})
    return 'usniete'


class Reminder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ##Events
    @commands.Cog.listener()
    async def on_ready(self):
        self.send_notification.start()
        self.actually_cal.start()
        print('bot is ready')

    # jesienna gawenda addon
    @commands.Cog.listener()  ##nie lubimy takich
    async def on_message(self, message):

        message_content = message.content.strip().lower()
        if gawena(message_content) == 1:
            typ = message.author

            teksty = ['Jebać jesienną gawendę', 'Dumny ty jesteś człowieku z tego co robisz?',
                      'Nawet ja nie dopuściłbym się czegoś takiego', 'Na Sigmara, dajcie tu ognia ', 'O kruca',
                      'Sigmarze ześlij na niego kometę']
            conte = random.choice(teksty)
            embed = discord.Embed()
            embed.set_author(name="Gosperd Behn ",
                             icon_url="https://static.wikia.nocookie.net/warhammerfb/images/2/25/Witch_Hunter_Generic.jpg/revision/latest/scale-to-width-down/340?cb=20170120024902")
            embed.add_field(name=typ, value=conte, inline=False)

            await message.channel.send(embed=embed)

        # tasks

    @tasks.loop(minutes=1)
    async def send_notification(self):
        channel = self.bot.get_channel(807716288675577908)

        minusdate = datetime.now() + timedelta(days=1)
        mention = {'Gracze I': '<@&491289891854876673>', 'Gracze II': '<@&647474242924970015>',
                   'Gracze III': '<@&681480093150871624>', 'Gracze IV': '<@&686997723358036053>'}
        for x in mycol.find({'date': {"$lt": minusdate}}):

            if x['date'] < (datetime.now() + timedelta(days=1)) and x['remebers'] == 0:

                await channel.send(mention[x['group']] + " Jutro sesja")
                mycol.update_one({'_id': x['_id']}, {"$set": {"remebers": 1}})
            elif x['date'] < (datetime.now() + timedelta(minutes=30)) and x['remebers'] == 1:

                await channel.send(mention[x['group']] + " 30 minut do grania")
                mycol.update_one({'_id': x['_id']}, {"$set": {"remebers": 2}})
            elif x['date'] < datetime.now() and x['remebers'] == 2:

                await channel.send(mention[x['group']] + " Sesjaaaaa!")
                mycol.delete_one({"_id": x['_id']})

    @tasks.loop(minutes=30)
    async def actually_cal(self):
        channel = self.bot.get_channel(807716288675577908)

        messageid = 810519866259931166
        response = (show_all_sesions())
        embed = discord.Embed(title="Aktualny kalendarz:")
        for x in response:
            timeto = str(abs(x['date'] - datetime.now())).split(".")[0]

            embed.add_field(name=x['date'], value='**Nazwa:** ' + x['name'] + '\n' + '**Grupa:** ' + x[
                'group'] + '\n' + '**Za:** ' + timeto, inline=False)
        msg = await channel.fetch_message(messageid)
        await msg.edit(embed=embed)

    ##Commands

    ##Make new sesion
    @commands.command(name='sesja', help='Dodaje sejse, nazwa grupa dd/mm/rr hh:mm.')
    async def sesja(self, ctx, *, sesja_parm):

        response = (add_new_sesion(sesja_parm))
        await ctx.send(response)

    ##Show all sesions
    @commands.command(name='sesje', help='Pokazuje wszystkie sesje.')
    async def sesje(self, ctx):
        response = (show_all_sesions())
        embed = discord.Embed(title="Wszystkie sesje:")
        for x in response:
            timeto = str(abs(x['date'] - datetime.now())).split(".")[0]

            embed.add_field(name=x['date'], value='**Nazwa:** ' + x['name'] + '\n' + '**Grupa:** ' + x[
                'group'] + '\n' + '**Za:** ' + timeto, inline=False)
        await ctx.send(embed=embed)

        ##Show all sesions

    @commands.command(name='moje sesje', help='Pokazuje sesje danej drużyny, po spacji kod drużyny')
    async def moje(self, ctx, *, group):
        response = (find_my_sesions(group))
        embed = discord.Embed(title="Wybrane sesje:")
        for x in response:
            timeto = str(abs(x['date'] - datetime.now())).split(".")[0]

            embed.add_field(name=x['date'], value='**Nazwa:** ' + x['name'] + '\n' + '**Za:** ' + timeto, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='kostka', help='r 1d10')  ##kostka
    async def r(self, ctx, *, x):
        elements, end = dice(x)
        embed = discord.Embed(title="Kostka co nie oszukuje:")
        embed.add_field(name='Wyniki: ', value=elements, inline=False)
        embed.add_field(name='Suma: ', value=end, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='usuń sesje', help='usuwa sesje, nazwa sesji data')
    async def usuns(self, ctx, *, x):
        response = delete_session(x)
        await ctx.send(response)

    @commands.command(name='wewnetrzny help', help='w sumie juz zbędny')  ##help
    async def sesjahelp(self, ctx):
        embed = discord.Embed(title="Komendy: ", description="bocik do sesji")
        embed.add_field(name="!sesja nazwa grupa data godzina",
                        value="tworzy nową sesję, nazwa nie może mieć spacji. grupy G1 do G4 data: dd/mm/rr godzina: hh/mm ",
                        inline=False)
        embed.add_field(name="!sesje", value="pokazuje wszystkie sesje", inline=False)
        embed.add_field(name="!moje  grupa", value="pokazuje sesje danej grupy ", inline=True)
        embed.add_field(name="!r (liczba)d(liczba)", value="kostka i tyle ", inline=True)
        embed.add_field(name="!usuns (nazwa) (dd/mm/rr hh:mm)", value="usuwa sesje ", inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Reminder(client))
