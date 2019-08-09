import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time, random

client = commands.Bot(command_prefix = "$")

@client.event 
async def on_ready():
    print("GQBot is online! Hail the Fathers!")
    
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def spam100(ctx):
    for i in range(100):
        await ctx.send("@everyone bow down to the GQEmpire")

"""
Still needs to be migrated
@commands.Cog.listener()
async def on_message(ctx, message):
    if message.content == "Greetings, GQBot!":
        await ctx.send_message(message.channel, "Hail the Fathers!")
    elif message.content == "greetings, GQBot!":
        await ctx.send_message(message.channel, "Hail the Fathers!")
    elif message.content == "greetings GQBot!":
        await ctx.send_message(message.channel, "Hail the Fathers!")
    await ctx.process_commands(message)
"""

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
    await ctx.send("http://gq-quests.atwebpages.com")

@client.command()
async def toss(ctx):
    await ctx.send("Tossing coin... It landed " + random.choice(("heads","tails"))+"!")

"""
Still needs to be migrated
@client.event
async def on_message(ctx, message):
    if message.content == "calm":
        await ctx.send_message(message.channel, "Do you know what else is calm?! The GQBot!")
    elif message.content == "calm.":
        await ctx.send_message(message.channel, "Do you know what else is calm?! The GQBot!")
    await client.process_commands(message)
"""
@client.command()
async def gqempire(ctx):
    await ctx.send("http://GQEmpire.gq")
    await ctx.send("This is your main site! Feel free to make it your homepage :)")

client.run("im-not-telling-you-the-token")
