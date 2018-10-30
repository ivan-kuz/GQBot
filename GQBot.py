import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time


Client = discord.Client()
client = commands.Bot(command_prefix = "$")


@client.event 
async def on_ready():
    print("GQBot is online! Hail the Fathers!")
    
@client.command()
async def ping():
    await client.say("Pong!")

@client.command()
async def spam100():
    n = 1
    while 1 < 101:
        await client.say("@everyone bow down to the GQEmpire")
        n += 1

@client.command()
async def romatime():
    await client.say("http://romatime.gq")
    await client.say("The most recent episode is: " + "https://www.youtube.com/watch?v=pUcxS8Cnyfg")

@client.command()
async def aquaesulis():
    await client.say("http://aquaesulis.gq")

@client.command()
async def tiffinbbc():
    await client.say("http://tiffinBBC.gq")
    await client.say("WARNING! Formatting might look relly weird on big screens!")
    
@client.command()
async def github():
    await client.say("https://github.com/ivan-kuz/GQBot/")
    await client.say("This is the github repo for the GQBot. If you're an avid coder, feel free to contribute to this wonderful bot!")
    
@client.command()
async def wiki():
    await client.say("https://github.com/ivan-kuz/GQBot/wiki")
    await client.say("This is the link to the wiki for the GQBot. If you need some help - you will definitely find it on there!")

@client.command()
async def quests():
    await client.say("Press 'Run' to play your first quest!")
    await client.say("http://gq-quests.atwebpages.com")

@client.event
async def on_message(message):
    if message.content == "calm":
        await client.send_message(message.channel, "Do you know what else is calm?! The GQBot!")
    elif message.content == "calm.":
        await client.send_message(message.channel, "Do you know what else is calm?! The GQBot!")
    await client.process_commands(message)
        
@client.command()
async def gqempire():
    await cleint.say("http://GQEmpire.gq")
    await client.say("This is your main site! Feel free to make it your homepage :)")

client.run("token")
