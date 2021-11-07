import discord
from discord.ext import commands
import asyncio
from tokens import disc_token

client = commands.Bot(command_prefix = '.')

def check(message: discord.Message, member):
    return isinstance(message.channel, discord.DMChannel) and message.author == member

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()   
async def dm(ctx, member : discord.Member, *, content: str):
    await member.send(content)
            
    try:
        await member.send("How would you like to respond to your Secret Santa?")
        reply = await client.wait_for("message", check = lambda message: isinstance(message.channel, discord.DMChannel) and message.author == member)
        await ctx.author.send(reply.content)
    except asyncio.TimeoutError:
        pass

client.run(disc_token)
