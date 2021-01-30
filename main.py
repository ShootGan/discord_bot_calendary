import os

from discord.ext import commands

from cogs.reminder import Reminder

client = commands.Bot(command_prefix='!')
TOKEN = os.getenv('KEY')
print(TOKEN)
if __name__ == '__main__':
    client.add_cog(Reminder(client))
    client.run(TOKEN)
