import discord
from discord.ext import commands
import asyncio
import random

from discord.ext.commands.converter import UserConverter
from tokens import disc_token
import db

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '.', intents=intents)

def check(message: discord.Message, member):
    return isinstance(message.channel, discord.DMChannel) and message.author == member

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()   
async def dm(ctx, user):
    server = await what_server(ctx)
    for person in server.members:
        if f"{person.name}#{person.discriminator}" == user:
            member = person
            break

    await ctx.send(embed = embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg","What is your message?"))
    reply = await client.wait_for("message", check = lambda message: message.author == ctx.author)
    await member.send(embed=embed("From Anonymous", "https://sandstormit.com/wp-content/uploads/2018/09/incognito-2231825_960_720-1-300x300.png", reply.content))
            
    try:
        await member.send("How would you like to respond?")
        reply = await client.wait_for("message", check = lambda message: isinstance(message.channel, discord.DMChannel) and message.author == member)
        await ctx.author.send(embed = embed(f"From {member.name}#{member.discriminator}", member.avatar_url,reply.content))
    except asyncio.TimeoutError:
        pass

@client.command()
async def secret_santa(ctx, *users):
    if users[0] == "all":
        updated_users = [user for user in ctx.message.guild.members if user.bot == False]
    else:
        updated_users = []
        for user in list(users):
            user = user.replace("<", "")
            user = user.replace(">", "")
            user = user.replace("!", "")
            user = user.replace("@", "")
            user = user.replace(",", "")
            new_user = await commands.UserConverter.convert(commands.UserConverter(), ctx, user)
            updated_users.append(new_user)
            
    random.shuffle(updated_users)
    
    # Key = Santa, Value = Recipient
    pairs = {}
    pairs[updated_users[len(updated_users) - 1].id] = updated_users[0].id
    
    # DM user at last spot that their person is the first person
    await ctx.send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", "You have been messaged your recipients!"))
    await updated_users[len(updated_users)-1].send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", f"Your person is {updated_users[0].name}#{updated_users[0].discriminator}."))

    for i in range(len(updated_users) - 1):
        # DM user that their recipient is user in next pos
        await updated_users[i].send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", f"Your person is {updated_users[i+1].name}#{updated_users[i+1].discriminator}"))
        # Store dict of users and recipients
        pairs[updated_users[i].id] = updated_users[i+1].id
    
    db.upload_pairs(ctx.message.guild, pairs)

@client.command()
async def dm_gifter(ctx):
    server = await what_server(ctx)
    pairs = db.get_pairs(server)
    i = list(pairs.values()).index(ctx.author.id)
    gifter = list(pairs.keys())[i]
    gifter = await commands.UserConverter.convert(commands.UserConverter(), ctx, gifter)
    await ctx.send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", "What is your message?"))
    reply = await client.wait_for("message", check = lambda message: message.author == ctx.author)
    await gifter.send(embed=embed("From Receiver", "https://cdn.discordapp.com/attachments/500075932581888010/906905035600977940/2Q.png", reply.content))

@client.command()
async def dm_receiver(ctx):
    server = await what_server(ctx)
    pairs = db.get_pairs(server)
    i = list(pairs.keys()).index(str(ctx.author.id))
    receiver = str(list(pairs.values())[i])
    receiver = await commands.UserConverter.convert(commands.UserConverter(), ctx, receiver)
    await ctx.send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", "What is your message?"))
    reply = await client.wait_for("message", check = lambda message: message.author == ctx.author)
    await receiver.send(embed=embed("From Santa", "https://cdn.discordapp.com/attachments/500075932581888010/906904927828344842/8QvJg34dYvAAAAABJRU5ErkJggg.png", reply.content))


def embed(author, author_icon, message):
    embed = discord.Embed()
    embed.set_thumbnail(url="https://www.pinclipart.com/picdir/middle/9-98228_present-gift-clipart-explore-pictures-gifts-clipart-png.png")
    embed.set_author(name=author, icon_url=author_icon)
    embed.add_field(name=message, value='\u200b')
    return embed

async def what_server(ctx):
    message = "Which server would you like to message someone in?"
    server_number = 0
    shared_servers = ctx.author.mutual_guilds
    for server in shared_servers:
        message += f"\n{server.name} : {server_number}"
        server_number += 1

    await ctx.send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg", message))
    try:
        reply = await client.wait_for("message", check = lambda message: message.author == ctx.author)
        return shared_servers[int(reply.content)]
    except:
        await ctx.send(embed=embed("From ElfBot", "https://cdn.discordapp.com/attachments/500075932581888010/906895479042887690/ElfBot_Thumbnail.jpg","Invalid input."))

client.run(disc_token)
