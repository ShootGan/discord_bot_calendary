import os

from discord.ext import commands

from cogs.reminder import Reminder

bot = commands.Bot(command_prefix='!')
TOKEN = os.getenv('KEY')

if __name__ == '__main__':
    bot.add_cog(Reminder(bot))
    bot.run(TOKEN)
