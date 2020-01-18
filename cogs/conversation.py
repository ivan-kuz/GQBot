from cogs.base import CogBase
from utils import regex
import re
import random
import asyncio
from utils.botconstants import PREFIX_RAW, MEE6_ID


def gen_goodbye(name, night=False):
    goodbye = random.choice(("Goodbye, ", "See you later, ", "Bye, "))
    goodbye += "{}. "
    goodbye += random.choice(("", "I'll be here.", "Have a nice day!"))
    return goodbye.format(name)


def gen_goodnight(name):
    goodnight = random.choice(("Night, ", "Goodnight, ", "Gn, "))
    goodnight += "{}. "
    goodnight += random.choice(("", "Sleep tight!", "Rest well!", "Don't let the bedbugs bite!", "Sweet dreams!"))
    return goodnight.format(name)


def gen_greeting(name):
    greeting = random.choice(("Hello, ", "Greetings, ", "Hey, ", "Long time no see, "))
    greeting += "{}. "
    greeting += random.choice(("", "How have you been?",
                               "Have you seen my new features?",
                               "Type {}help to see my commands.".format(PREFIX_RAW),
                               "What's up?"))
    return greeting.format(name)


class ConvoCog(CogBase, name="Conversation"):
    """Dodgy stabs at natural speech."""

    COLOUR = 0x111111
    
    hidden = True
    
    @CogBase.listener()
    async def on_message(self, message):
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
        if re.search("calm", message_content):
            await message.channel.send("Do you know what else is calm?! The GQBot!")
        if message_content == "hello there!":
            await message.channel.send("General Kenobi!")
            await asyncio.sleep(1)
            await message.channel.send("You *are* a bold one!")
        if regex.BOT_MENTION.search(message_content):
            display_name = message.author.display_name
            if regex.GREETING.search(message_content):
                await message.channel.send(gen_greeting(display_name))
            elif regex.FAREWELL.search(message_content):
                await message.channel.send(gen_goodbye(display_name))
            elif regex.NIGHT.search(message_content):
                await message.channel.send(gen_goodnight(display_name))
