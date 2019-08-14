import discord
from discord.ext.commands import *
from discord.ext.commands.errors import *
from discord.ext import commands
import asyncio
import time, random, re
import games.snake as snake
from botconstants import *

client = commands.Bot(command_prefix = PREFIX)
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
@has_permissions(mention_everyone=True)
@commands.cooldown(1,3600)
async def spam100(ctx):
    """Spam pings everyone 100 times."""
    for i in range(100):
        await ctx.send("@everyone bow down to the GQEmpire")
        await asyncio.sleep(2)
    
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
@formatdoc
async def roll(ctx, *args):
    """Rolls dice, or picks a choice at random.

{0}roll --> rolls a single 6-sided die
{0}roll x --> rolls a single x-sided die
{0}roll x y --> rolls y x-sided dice
{0}roll a b c d ... --> outputs one of the choices at random

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
    eyerolls = 0
    if message.author != client.user:
        for c in messageContent:
            if c == "🙄":
                eyerolls += 1
    if eyerolls > 0:
        ts = "> "
        for er in range(eyerolls):
            ts += "🙄"
        ts += "\n"
        for er in range(eyerolls):
            ts += "😎"
        await message.channel.send(ts)
    if message.channel in suggChannels:
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    if re.search("GG .*, you just advanced to level .*!", message.content) != None:
        await message.add_reaction("🖕")
        await message.channel.send("Shut up, bot.")
    if messageContent == "calm":
        await message.channel.send("Do you know what else is calm?! The GQBot!")
    if messageContent == "hello there!":
        await message.channel.send("General Kenobi!")
        await asyncio.sleep(1)
        await message.channel.send("You *are* a bold one!")
    if re.search("^((h+e+ll+o+)|(gr+ee+ti+n+gs+)|(hi+)|(h+e+y+)|(((wa)|')?s+u+p+)|(y+o+)|(szia))\\b", messageContent) != None and re.search("\\b((bot)|(gqbot)|(lilgq))\\b", messageContent) != None and re.search("\\b(bot)|(gqbot)|(lilgq)", message.author.display_name) == None:
        await message.channel.send(await gen_greeting(message.author.display_name))
    if re.search("^(((c|(see)) ?y((a+)|(ou)))|((goo+d)?(by+e+))|((g((ood)?)(.?))?n+(i((te)|(ght)))?)|(おやすみ(なさい)?)|(farewell))\\b", messageContent) != None and re.search("\\b((bot)|(gqbot)|(lilgq))\\b", messageContent) != None and re.search("\\b(bot)|(gqbot)|(lilgq)", message.author.display_name) == None:
        await message.channel.send(await gen_goodbye(message.author.display_name, re.search("^(((g((ood)?)(.?))?n+(i((te)|(ght)))?)|(おやすみ(なさい)?))\\b", messageContent) != None))
    await client.process_commands(message)

async def gen_goodbye(name, night=False):
    goodbye = random.choice(("Goodbye, ", "See you later, ", "Bye, ") if not night else ("Night, ", "Goodnight, ", "Gn, "))
    goodbye += "{}. "
    goodbye += random.choice(("", "I'll be here.", "Have a nice day!") if not night else ("", "Sleep tight!", "Rest well!", "Don't let the bedbugs bite!", "Sweet dreams!"))
    return goodbye.format(name)

async def gen_greeting(name):
    greeting = random.choice(("Hello, ", "Greetings, ", "Hey, ", "Long time no see, "))
    greeting += "{}. "
    greeting += random.choice(("", "How have you been?", "Have you seen my new features?", "Type {}help to see my commands.".format(PREFIX_RAW), "What's up?"))
    return greeting.format(name)

@client.event
async def on_raw_reaction_add(payload) -> "Automatic Pins":
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

@client.group(aliases=["roles"])
async def role(ctx):
    """Role managing commands.

Must have manage_roles permission to use."""
    pass

@role.command(name="add")
@has_permissions(manage_roles=True)
@formatdoc
async def role_add(ctx, rec:discord.Member, role:discord.Role):
    """Give a user an existing role.

{}role add user role --> gives user the given role

Must have role managing permissions."""
    await rec.add_roles(role)
    await ctx.send("Gave "+rec.mention+" the role "+role.name+".")

@role.command(name="create")
@has_permissions(manage_roles=True)
@formatdoc
async def role_create(ctx, rname, copyFrom:discord.Role=None):
    """Create a new role.

{0}role create name --> makes a new role called "name"
{0}role create name other_role --> makes a new role called "name" with the same perms as other_role

Must have role managing permissions."""
    if copyFrom == None:
        await ctx.guild.create_role(name=rname)
    else:
        await ctx.guild.create_role(name=rname, permissions=copyFrom.permissions)
    await ctx.send("Created new role: "+rname)

@role.command(name="edit")
@has_permissions(manage_roles=True)
@formatdoc
async def role_edit(ctx, role:discord.Role):
    """Edit existing role.

{}role edit name --> opens Role Editor

Role Editor
Shows a list of 10 permissions on each page.
Members with manage_roles permissions can react with the respective emoji to toggle the permission.
React with ▶ to move to the next page.
React with ❌ to close the editor."""
    reactants = ["0⃣","1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣","▶","❌"]
    async with ctx.typing():
        registers = []
        currReg = []
        c = 0
        for pair in iter(role.permissions):
            currReg.append(pair[0])
            c+=1
            if c == 10:
                c = 0
                registers.append(currReg[:])
                currReg = []
        registers.append(currReg[:])
        regIndex = 0
        msg = None
        async def updateEmbed():
            ret = ""
            pDict = dict(list(iter(role.permissions)))
            for i, r in enumerate(registers[regIndex]):
                ret += reactants[i]+" "+r+" "+("✅" if pDict[r] else "❎")+"\n"
            return ret
        def check(reaction, user):
            return user != msg.author and user.permissions_in(msg.channel).manage_roles and reaction.message.id == msg.id
        while True:
            d=await updateEmbed()
            e=discord.Embed(title="Editing role: "+role.name, description=d, colour=0x00ff00)
            e.set_footer(text="Role Editor")
            if msg == None:
                msg = await ctx.send(embed=e)
                for e in reactants:
                    await msg.add_reaction(e)
            else:
                await msg.edit(embed=e)
            try:
                reaction, user = await client.wait_for('reaction_add', check=check)
            except asyncio.TimeoutError:
                msg.delete()
                return
            if reaction.emoji == "❌":
                await msg.delete()
                return
            if reaction.emoji == "▶":
                regIndex += 1
                if regIndex >= len(registers)-1:
                    regIndex = 0
                await reaction.remove(ctx.author)
            elif reaction.emoji in reactants:
                perm = registers[regIndex][reactants.index(reaction.emoji)]
                setattr(role.permissions, perm, not getattr(role.permissions, perm))
                await reaction.remove(user)

@client.command(name="snake")
async def play_snake(ctx, magic="no"):
    """Play snake.

Communist edition."""
    reactants = ["🔼","🔽","◀","▶"]
    snakeGame = snake.Game()
    if magic == "communist":
        snakeGame.apple = (-1,-1)
        snakeGame.render()
    botmsg = await ctx.send("```{}```".format(snakeGame.renderString))
    for reactant in reactants:
        await botmsg.add_reaction(reactant)
    while snakeGame.running:
        msg = await ctx.fetch_message(botmsg.id)
        timer = time.time()
        commandments = {0:0,1:0,2:0,3:0}
        for reaction in msg.reactions:
            async for user in reaction.users():
                if user != client.user:
                    await reaction.remove(user)
                    if reaction.emoji in reactants:
                        commandments[reactants.index(reaction.emoji)]+=1
        vote = max(commandments.keys(), key=lambda x: commandments[x])
        if commandments[vote] > 0:
            snakeGame.xVect, snakeGame.yVect = ((0,-1),(0,1),(-1,0),(1,0))[vote]
        msg = await ctx.fetch_message(botmsg.id)
        snakeGame.update()
        gameS = "```{}```".format(snakeGame.renderString)
        await msg.edit(content=gameS)
        await asyncio.sleep(timer+1-time.time())
    e = discord.Embed(title="Game Over!", description="Ended game with length: "+str(len(snakeGame.snake)), colour=0x3232ef)
    e.set_footer(text="{}snake to play again".format(PREFIX_RAW))
    await msg.edit(content="",embed=e)
        

@client.listen()
async def on_command_error(ctx, error):
        error = error.__cause__ or error
        if isinstance(error, CommandNotFound):
            e = discord.Embed(title="I didn't quite catch that.", description="Maybe look at my help menu if you're stuck?", colour=0xec6761)
            e.set_footer(text='{}help'.format(PREFIX_RAW))
            await ctx.send(embed=e)
        elif isinstance(error, MissingPermissions):
            e=discord.Embed(title='Wait. That\'s illegal.', description='You don\'t have the right permissions for that, buddy.', colour=0xec6761)
            e.set_footer(text=str(error))
            await ctx.send(embed=e)
        elif isinstance(error, BadArgument):
            if ctx.message.content[:8+PREFIXLEN].lower() == "{}role add".format(PREFIX_RAW):
                await ctx.send(embed=discord.Embed(title="Role or user doesn't exist.", description="You'll have to create a new role yourself using {}role create, or check for mistakes.".format(PREFIX_RAW), colour=0xec6761))
        elif isinstance(error, asyncio.TimeoutError):
            await ctx.send(embed=discord.Embed(title="Timed out.", description="I waited for a while but it seems the time is up.", colour=0xec6761))
        elif isinstance(error, CommandOnCooldown):
            e=discord.Embed(title='I have a cooldown, you know!', description='That command has a cooldown.', colour=0xec6761)
            e.set_footer(text=str(error))
            await ctx.send(embed=e)
        else:
            e = discord.Embed(title="Beep boop.", description="That threw an error I didn't quite catch. Don't worry, I'm fine though.", colour=0xec6761)
            e.set_footer(text=str(error))
            await ctx.send(embed=e)

client.run("not_telling_you_the_token")
