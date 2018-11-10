import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time


Client = discord.Client()
client = commands.Bot(command_prefix = "?")


@client.event 
async def on_ready():
    print("Bot is online and connected to Discord")
    
@client.command()
async def ping():
    await client.say("Pong!")
    
@client.command()
async def echo(*args):
    output = ""
    for word in args:
        output += word
        output += " "
    await client.say(output)

client.run("token")
