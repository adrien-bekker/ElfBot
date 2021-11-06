import discord
from discord.ext import commands

client = commands.bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

client.run('OTA2NjMyNDIzNDA2NzE5MDU2.YYbdPg.9eeo7ZkATMYjm_Pr3pKWNiLoPM8')
