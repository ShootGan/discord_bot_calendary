import discord
from discord.ext import commands
from token_r import read_token
from cogs.reminder import Reminder
client = commands.Bot(command_prefix='!')
TOKEN= read_token()
if __name__ == '__main__':
    client.add_cog(Reminder(client))
    client.run(TOKEN)
