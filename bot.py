import discord
from discord.ext import commands
from tokens import disc_token

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

client.run(disc_token)
