import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import time
import random
import re
import games.snake as snake
import regex
from botconstants import *
import cogs

bot = commands.Bot(command_prefix=PREFIX)
suggestion_channels = []
PIN_REACTIONS_MIN = 3
EMOJI = json.load(open("emoji.json", "r"))

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
async def on_raw_reaction_add(payload) -> "Automatic Pins":
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


@bot.group(name="role", aliases=["roles"])
async def role_group(_):
    """Role managing commands.

    Must have manage_roles permission to use."""
    pass


@role_group.command(name="add")
@commands.has_permissions(manage_roles=True)
@format_doc
async def role_add(ctx, rec: discord.Member, role: discord.Role):
    """Give a user an existing role.

    {}role add user role --> gives user the given role

    Must have role managing permissions."""
    await rec.add_roles(role)
    await ctx.send("Gave "+rec.mention+" the role "+role.name+".")


@role_group.command(name="create")
@commands.has_permissions(manage_roles=True)
@format_doc
async def role_create(ctx, r_name, copy_from: discord.Role = None):
    """Create a new role.

    {0}role create name --> makes a new role called "name"
    {0}role create name other_role --> makes a new role called "name" with the same perms as other_role

    Must have role managing permissions."""
    if copy_from is None:
        await ctx.guild.create_role(name=r_name)
    else:
        await ctx.guild.create_role(name=r_name, permissions=copy_from.permissions)
    await ctx.send("Created new role: " + r_name)


@role_group.command(name="edit")
@commands.has_permissions(manage_roles=True)
@format_doc
async def role_edit(ctx, role: discord.Role):
    """Edit existing role.

    {}role edit name --> opens Role Editor

    Role Editor
    Shows a list of 10 permissions on each page.
    Members with manage_roles permissions can react with the respective emoji to toggle the permission.
    React with ▶ to move to the next page.
    React with ❌ to close the editor."""
    reactants = EMOJI["DIGITS"] + [EMOJI["ARROWS"]["RIGHT"], EMOJI["CROSS_RED"]]
    async with ctx.typing():
        registers = []
        curr_reg = []
        c = 0
        for pair in role.permissions:
            curr_reg.append(pair[0])
            c += 1
            if c == 10:
                c = 0
                registers.append(curr_reg[:])
                curr_reg = []
        registers.append(curr_reg[:])
        reg_index = 0
        msg = None

        async def update_embed():
            ret = ""
            p_dict = dict(list(iter(role.permissions)))
            for i, r in enumerate(registers[reg_index]):
                ret += reactants[i]+" "+r+" "+(EMOJI["TICK"] if p_dict[r] else EMOJI["CROSS_BLUE"])+"\n"
            return ret

        def c_check(c_reaction, c_user):
            return (c_user != msg.author and
                    c_user.permissions_in(msg.channel).manage_roles and
                    c_reaction.message.id == msg.id)

        while True:
            d = await update_embed()
            e = discord.Embed(title="Editing role: "+role.name, description=d, colour=0x00ff00)
            e.set_footer(text="Role Editor")
            if msg is None:
                msg = await ctx.send(embed=e)
                for e in reactants:
                    await msg.add_reaction(e)
            else:
                await msg.edit(embed=e)
            try:
                reaction, user = await bot.wait_for('reaction_add', check=c_check)
            except asyncio.TimeoutError:
                msg.delete()
                return
            if reaction.emoji == EMOJI["CROSS_RED"]:
                await msg.delete()
                return
            if reaction.emoji == EMOJI["ARROW"]["RIGHT"]:
                reg_index += 1
                if reg_index >= len(registers)-1:
                    reg_index = 0
                await reaction.remove(ctx.author)
            elif reaction.emoji in reactants:
                perm = registers[reg_index][reactants.index(reaction.emoji)]
                setattr(role.permissions, perm, not getattr(role.permissions, perm))
                await reaction.remove(user)


@bot.command(name="snake")
async def play_snake(ctx, magic="no"):
    """Play snake.

    Communist edition."""
    reactants = EMOJI["ARROWS"]["ARRAY"]
    snake_game = snake.Game()

    if magic == "communist":
        snake_game.apple = (-1, -1)
        snake_game.render()

    bot_msg = await ctx.send("```{}```".format(snake_game.render_string))
    for reactant in reactants:
        await bot_msg.add_reaction(reactant)

    msg = await ctx.fetch_message(bot_msg.id)
    while snake_game.running:
        timer = time.time()
        commandments = {0: 0, 1: 0, 2: 0, 3: 0}
        for reaction in msg.reactions:
            async for user in reaction.users():
                if user != bot.user:
                    await reaction.remove(user)
                    if reaction.emoji in reactants:
                        commandments[reactants.index(reaction.emoji)] += 1
        vote = max(commandments.keys(), key=lambda x: commandments[x])
        if commandments[vote] > 0:
            snake_game.x_vect, snake_game.y_vect = ((0, -1), (0, 1), (-1, 0), (1, 0))[vote]
        snake_game.update()
        game_s = "```{}```".format(snake_game.render_string)
        await msg.edit(content=game_s)
        await asyncio.sleep(timer+1-time.time())
    e = discord.Embed(title="Game Over!",
                      description="Ended game with length: "+str(len(snake_game.snake)), colour=0x3232ef)
    e.set_footer(text="{}snake to play again".format(PREFIX_RAW))
    await msg.edit(content="", embed=e)
        

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
