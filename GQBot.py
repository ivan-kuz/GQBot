import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time, random, re

client = commands.Bot(command_prefix = "$")
suggChannels = []
PIN_REACTIONS_MIN = 3

@client.event 
async def on_ready():
    print("GQBot is online! Hail the Fathers!")
    global suggChannels
    suggChannels = []
    for c in client.get_all_channels():
        if c.name == "suggestions":
            suggChannels.append(c)

@client.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send("Pong!")

@client.command()
async def hail(ctx):
    """Hails the fathers."""
    await ctx.send("Hail the fathers!")

@client.command()
async def spam100(ctx):
    """Spam pings everyone 100 times."""
    for i in range(100):
        await ctx.send("@everyone bow down to the GQEmpire")
    
@client.command()
async def romatime(ctx):
    """Link to romatime.gq"""
    await ctx.send("http://romatime.gq")
    await ctx.send("The most recent episode is: " + "https://www.youtube.com/watch?v=pUcxS8Cnyfg")

@client.command()
async def aquaesulis(ctx):
    """Link to aquaesulis.gq"""
    await ctx.send("http://aquaesulis.gq")

@client.command()
async def tiffinbbc(ctx):
    """Link to tiffinbbc.gq"""
    await ctx.send("http://tiffinBBC.gq")
    await ctx.send("WARNING! Formatting might look really weird on big screens!")
    
@client.command()
async def github(ctx):
    """Link to GQBot's Github repo."""
    await ctx.send("https://github.com/ivan-kuz/GQBot/")
    await ctx.send("This is the github repo for the GQBot. If you're an avid coder, feel free to contribute to this wonderful bot!")
    
@client.command()
async def wiki(ctx):
    """Link to GQBot's Github wiki."""
    await ctx.send("https://github.com/ivan-kuz/GQBot/wiki")
    await ctx.send("This is the link to the wiki for the GQBot. If you need some help - you will definitely find it on there!")

@client.command()
async def quests(ctx):
    """Link to quests.gq"""
    await ctx.send("Press 'Run' to play your first quest!")
    await ctx.send("http://quests.aquaesulis.gq")

@client.command()
async def toss(ctx):
    """Tosses a coin."""
    await ctx.send("Tossing coin... It landed " + random.choice(("heads","tails"))+"!")

@client.command()
async def flip(ctx):
    """Flips a coin."""
    await ctx.send("Flipping coin... It landed " + random.choice(("heads","tails"))+"!")

@client.command()
async def roll(ctx, *args):
    """Rolls dice, or picks a choice at random.

$roll --> rolls a single 6-sided die
$roll x --> rolls a single x-sided die
$roll x y --> rolls y x-sided dice
$roll a b c d ... --> outputs one of the choices at random

If any values for the second and third commands are invalid, they default to x=6; y=1."""
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
    if re.search("^((h+e+ll+o+)|(gr+ee+ti+n+gs+)|(hi+)|(h+e+y+)|(((wa)|')?s+u+p+)|(y+o+))\\b", messageContent) != None and re.search("\\b((bot)|(gqbot)|(lilgq))\\b", messageContent) != None and re.search("\\b(bot)|(gqbot)|(lilgq)", message.author.display_name) == None:
        await message.channel.send("Hello, {}!".format(message.author.display_name))
    await client.process_commands(message)

@client.event
async def on_raw_reaction_add(payload) -> "Automatic Pins":
    f"""If a message receives {PIN_REACTIONS_MIN} 📌 reactions, pin the message, or if someone with pinning permissions reacts with it."""
    if str(payload.emoji) == "📌":
        msgId = payload.message_id
        channelId = payload.channel_id
        channel = client.get_channel(channelId)
        if channel == None:
            return
        msg = await channel.fetch_message(msgId)
        if msg.pinned:
            return
        reaction = list(filter(lambda x: str(x.emoji)=="📌", msg.reactions))[0]
        cn = 0
        async for user in reaction.users():
            cn += 1
            if cn >= PIN_REACTIONS_MIN or user.permissions_in(channel).manage_messages:
                await msg.pin()
                break

@client.command()
async def gqempire(ctx):
    """Links to GQEmpire.gq"""
    await ctx.send("http://GQEmpire.gq")
    await ctx.send("This is your main site! Feel free to make it your homepage :)")

client.run("not_telling_you_the_token")
