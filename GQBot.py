import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import random
import re
import regex
from botconstants import *
import cogs

bot = commands.Bot(command_prefix=PREFIX)
suggestion_channels = []
PIN_REACTIONS_MIN = 3

for cog in cogs.COGS:
    bot.add_cog(cog(bot))


@bot.event
async def on_ready():
    print("GQBot is online! Hail the Fathers!")
    global suggestion_channels
    suggestion_channels = []
    for c in bot.get_all_channels():
        if c.name == "suggestions":
            suggestion_channels.append(c)


@bot.event
async def on_message(message):
    if message.author.bot and message.author.id != MEE6_ID:  # Return if the author is a bot, unless it is MEE6.
        return
    message_content = message.content.lower()
    if EMOJI["EYE_ROLL"] in message_content:
        reply = "> {}\n".format(message.content)
        reply += re.sub(EMOJI["EYE_ROLL"], EMOJI["SUNGLASSES"], message_content)
        await message.channel.send(reply)
        await message.add_reaction(EMOJI["SUNGLASSES"])
    if message.channel in suggestion_channels:
        await message.add_reaction(EMOJI["THUMBS_UP"])
        await message.add_reaction(EMOJI["THUMBS_DOWN"])
    if regex.MEE6.search(message.content):
        await message.add_reaction(EMOJI["MIDDLE_FINGER"])
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


@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == EMOJI["PIN"]:
        msg_id = payload.message_id
        channel_id = payload.channel_id
        channel = bot.get_channel(channel_id)
        if channel is None:
            return
        msg = await channel.fetch_message(msg_id)
        if msg.pinned:
            return
        reaction = list(filter(lambda x: str(x.emoji) == EMOJI["PIN"], msg.reactions))[0]
        cn = 0
        async for user in reaction.users():
            cn += 1
            if cn >= PIN_REACTIONS_MIN or user.permissions_in(channel).manage_messages:
                await msg.pin()
                break
        

ERROR_COLOR = 0xec6761


@bot.listen()
async def on_command_error(ctx, error):
    error = error.__cause__ or error
    if isinstance(error, CommandNotFound):
        e = discord.Embed(title="I didn't quite catch that.",
                          description="Maybe look at my help menu if you're stuck?", colour=ERROR_COLOR)
        e.set_footer(text='{}help'.format(PREFIX_RAW))
        await ctx.send(embed=e)
    elif isinstance(error, MissingPermissions):
        e = discord.Embed(title='Wait. That\'s illegal.',
                          description='You don\'t have the right permissions for that, buddy.', colour=ERROR_COLOR)
        e.set_footer(text=str(error))
        await ctx.send(embed=e)
    elif isinstance(error, BadArgument):
        if ctx.message.content[:8 + PREFIX_LEN].lower() == "{}role add".format(PREFIX_RAW):
            await ctx.send(embed=discord.Embed(title="Role or user doesn't exist.",
                           description="You'll have to create a new role yourself, " +
                           "using {}role create, or check for mistakes.".format(PREFIX_RAW),
                                               colour=ERROR_COLOR))
    elif isinstance(error, asyncio.TimeoutError):
        await ctx.send(embed=discord.Embed(title="Timed out.",
                                           description="I waited for a while but it seems the time is up.",
                                           colour=ERROR_COLOR))
    elif isinstance(error, CommandOnCooldown):
        e = discord.Embed(title='I have a cool-down, you know!', description='That command has a cool-down.',
                          colour=ERROR_COLOR)
        e.set_footer(text=str(error))
        await ctx.send(embed=e)
    else:
        e = discord.Embed(title="Beep boop.",
                          description="That threw an error I didn't quite catch. Don't worry, I'm fine though.",
                          colour=ERROR_COLOR)
        e.set_footer(text=str(error))
        await ctx.send(embed=e)

bot.run(TOKEN)
