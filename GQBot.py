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

@client.event
async def on_message(message):
    if message.content == "Greetings, GQBot!":
        await client.send_message(message.channel, "Hail the Fathers!")
    elif message.content == "greetings, GQBot!":
        await client.send_message(message.channel, "Hail the Fathers!")
    elif message.content == "greetings GQBot!":
        await client.send_message(message.channel, "Hail the Fathers!")
    await client.process_commands(message)

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

client.run("NDYyMzUwNjcyMzM2MTI1OTU4.Dhl1WQ.FFyRBQUoF_Jzp0Or7qP9GkRlFi4")
