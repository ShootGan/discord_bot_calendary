import discord
from discord.ext import commands
from token_r import start_functions11
from cogs.reminder import Reminder
client = commands.Bot(command_prefix='!')
TOKEN= start_functions11.read_token()
if __name__ == '__main__':
    start_functions11.create_table()
    client.add_cog(Reminder(client))
    client.run(TOKEN)
