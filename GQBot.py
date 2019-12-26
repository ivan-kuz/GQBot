import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import random
import re
from utils import regex, BarHelper
from utils.botconstants import *
import cogs

print("Finished imports!")

bot = commands.Bot(command_prefix=PREFIX)

print("Loading cogs...")
_bh = BarHelper(cogs.COG_COUNT)
_bh.print()
for cog in cogs.COGS:
    _bh.progress(end=f" {cog.__name__}\n")
    bot.add_cog(cog(bot))
print("Loaded cogs!")

@bot.event
async def on_ready():
    print("...GQBot is online!\nHail the Fathers!")


@bot.event
async def on_connect():
    print("Connected...")


@bot.event
async def on_disconnect():
    print("Lost connection.")


@bot.event
async def on_message(message):
    if message.author.bot and message.author.id != MEE6_ID:  # Return if the author is a bot, unless it is MEE6.
        return
    message_content = message.content.lower()
    if f"\N{FACE WITH ROLLING EYES}" in message_content:
        reply = "> {}\n".format(message.content)
        reply += re.sub(f"\N{FACE WITH ROLLING EYES}", f"\N{SMILING FACE WITH SUNGLASSES}", message_content)
        await message.channel.send(reply)
        await message.add_reaction(f"\N{SMILING FACE WITH SUNGLASSES}")
    if regex.MEE6.search(message.content):
        await message.add_reaction(f"\N{REVERSED HAND WITH MIDDLE FINGER EXTENDED}")
        await message.channel.send("Shut up, bot.")
    if message_content == "calm":
        await message.channel.send("Do you know what else is calm?! The GQBot!")
    if message_content == "hello there!":
        await message.channel.send("General Kenobi!")
        await asyncio.sleep(1)
        await message.channel.send("You *are* a bold one!")
    if regex.BOT_MENTION.search(message_content):
        display_name = message.author.display_name
        if regex.GREETING.search(message_content):
            await message.channel.send(await gen_greeting(display_name))
        if regex.FAREWELL.search(message_content):
            await message.channel.send(await gen_goodbye(display_name, bool(regex.NIGHT.search(message_content))))
    await bot.process_commands(message)


async def gen_goodbye(name, night=False):
    goodbye = random.choice(("Goodbye, ", "See you later, ", "Bye, ")
                            if not night else
                            ("Night, ", "Goodnight, ", "Gn, "))
    goodbye += "{}. "
    goodbye += random.choice(("", "I'll be here.", "Have a nice day!")
                             if not night else
                             ("", "Sleep tight!", "Rest well!", "Don't let the bedbugs bite!", "Sweet dreams!"))
    return goodbye.format(name)


async def gen_greeting(name):
    greeting = random.choice(("Hello, ", "Greetings, ", "Hey, ", "Long time no see, "))
    greeting += "{}. "
    greeting += random.choice(("", "How have you been?",
                               "Have you seen my new features?",
                               "Type {}help to see my commands.".format(PREFIX_RAW),
                               "What's up?"))
    return greeting.format(name)


bot.run(TOKEN)
