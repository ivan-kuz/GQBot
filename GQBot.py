import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time, random, re

client = commands.Bot(command_prefix = "$")
suggChannels = []

@client.event 
async def on_ready():
    print("GQBot is online! Hail the Fathers!")
    global suggChannels
    for c in client.get_all_channels():
        if c.name == "suggestions":
            suggChannels.append(c)
    
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def hail(ctx):
    await ctx.send("Hail the fathers!")

@client.command()
async def spam100(ctx):
    for i in range(100):
        await ctx.send("@everyone bow down to the GQEmpire")
    
@client.command()
async def romatime(ctx):
    await ctx.send("http://romatime.gq")
    await ctx.send("The most recent episode is: " + "https://www.youtube.com/watch?v=pUcxS8Cnyfg")

@client.command()
async def aquaesulis(ctx):
    await ctx.send("http://aquaesulis.gq")

@client.command()
async def tiffinbbc(ctx):
    await ctx.send("http://tiffinBBC.gq")
    await ctx.send("WARNING! Formatting might look really weird on big screens!")
    
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/ivan-kuz/GQBot/")
    await ctx.send("This is the github repo for the GQBot. If you're an avid coder, feel free to contribute to this wonderful bot!")
    
@client.command()
async def wiki(ctx):
    await ctx.send("https://github.com/ivan-kuz/GQBot/wiki")
    await ctx.send("This is the link to the wiki for the GQBot. If you need some help - you will definitely find it on there!")

@client.command()
async def quests(ctx):
    await ctx.send("Press 'Run' to play your first quest!")
    await ctx.send("http://quests.aquaesulis.gq")

@client.command()
async def toss(ctx):
    await ctx.send("Tossing coin... It landed " + random.choice(("heads","tails"))+"!")

@client.command()
async def roll(ctx, *args):
    dice = 1
    sides = None
    if len(args) == 0:
        sides = 6
    elif len(args) == 1:
        try:
            sides = int(args[0])
            if sides < 1:
                sides = 6
        except ValueError:
            sides = 6
    elif len(args) == 2:
        try:
            sides = int(args[0])
            dice = int(args[1])
            if sides < 1:
                sides = 6
            if dice < 1:
                dice = 1
        except ValueError:
            sides = None
            choices = args
    else:
        choices = args
    if sides == None:
        roll = '"'+random.choice(choices)+'"'
        flavour = "between "+str(len(choices))+" choices. "
    else:
        roll = 0
        for i in range(dice):
            roll += random.randint(1, sides)
        roll = str(roll)
        flavour = str(sides) + " sided di"
        if dice == 1:
            flavour += "e. "
        else:
            flavour += "ce, "+str(dice)+" of them. "
    await ctx.send("Rolling " + flavour + "Landed: " + roll)
    
@client.event
async def on_message(message):
    messageContent = message.content.lower()
    if message.channel in suggChannels:
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    if re.search("GG .*, you just advanced to level .*!", message.content) != None:
        await message.add_reaction("🖕")
        await message.channel.send("Shut up, bot.")
    if messageContent == "calm":
        await message.channel.send("Do you know what else is calm?! The GQBot!")
    if re.search("^((hello)|(greetings)|(hi))", messageContent) != None and re.search("\\b((bot)|(gqbot)|(lilgq))\\b", messageContent) != None and re.search("\\b(bot)|(gqbot)|(lilgq)", message.author.display_name) == None:
        await message.channel.send("Hello, "+message.author.display_name+"!")
    await client.process_commands(message)

@client.command()
async def gqempire(ctx):
    await ctx.send("http://GQEmpire.gq")
    await ctx.send("This is your main site! Feel free to make it your homepage :)")

client.run("not_telling_you_the_token")
