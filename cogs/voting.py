import inspect
import asyncio
import discord
from discord.ext.commands import Greedy
from discord.colour import Colour

from cogs.base import CogBase
from utils import format_doc, react_for
from utils.filters import *
from discord.ext import commands
from utils.botconstants import VOTING_CHANNELS, PIN_REACTIONS_MIN, EMOJI
from itertools import cycle
import numpy as np


def react_handler(filt, watch):
    def wrapper(coro):
        assert asyncio.iscoroutinefunction(coro), "Handler must be a coroutine function"
        setattr(coro, "__react_handler_for__", (filt, watch))
        return coro
    return wrapper


def is_handler(obj):
    try:
        _ = obj.__react_handler_for__
        return True
    except AttributeError:
        return False


def fill_between(start, end, char="\N{FULL BLOCK}", blank=" ", length=20):
    assert end >= start
    blank_start = round(start*length)
    center = round((end - start) * 20)
    blank_end = 20 - (blank_start + center)
    built = r"*|"
    built += blank*blank_start
    built += char*center
    built += blank*blank_end
    built += r"|*"
    return built


ANTI_RAINBOW = (Colour(0xff0000), Colour(0x00ff00), Colour(0x0000ff),
                Colour(0xffff00), Colour(0xff00ff), Colour(0x00ffff))


class VotingCog(CogBase, name="Voting"):
    """Voting and polls."""

    COLOUR = 0x008888
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
        self.handlers = {"CHANGE": [],
                         "REACTION_ADD": [],
                         "REACTION_REMOVE": []}
        for _, handler in inspect.getmembers(self, is_handler):
            filt, add_to = handler.__react_handler_for__
            self.handlers[add_to].append((handler, filt))
    
    @staticmethod
    async def set_vote(message):
        if not message.author.bot:
            await message.add_reaction(f"\N{THUMBS UP SIGN}")
            await message.add_reaction(f"\N{THUMBS DOWN SIGN}")
    
    @CogBase.listener()
    async def on_ready(self):
        """Set votes for messages sent when bot was offline."""
        for c_id in VOTING_CHANNELS:
            channel = self.bot.get_channel(c_id)
            async for msg in channel.history():
                if any(map(lambda x: x.me, msg.reactions)):
                    break
                await self.set_vote(msg)
    
    @CogBase.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id in VOTING_CHANNELS:
            await self.set_vote(message)
    
    @CogBase.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_event(event_type="REACTION_ADD", **(await self.unpack_payload(payload)))
    
    @CogBase.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_event(event_type="REACTION_REMOVE",
                                **(await self.unpack_payload(payload)))
    
    @react_handler(FilterFor(f"\N{PUSHPIN}"), "CHANGE")
    async def pin_handler(self, reactions, *, message, channel, event_type, **_):
        if event_type == "REACTION_ADD" and not message.pinned:
            reaction = reactions[0]
            users = await reaction.users().flatten()
            if len(users) >= PIN_REACTIONS_MIN or \
               any(map(lambda x: x.permissions_in(channel).manage_messages, users)):
                await message.pin()
            async for msg in channel.history():
                if msg.type == discord.MessageType.pins_add:
                    await msg.delete(delay=2)
                    break
    
        elif event_type == "REACTION_REMOVE" and message.pinned:
            if not reactions:
                await message.unpin()
                return
            reaction = reactions[0]
            users = await reaction.users().flatten()
            if len(users) <= PIN_REACTIONS_MIN and not \
               any(map(lambda x: x.permissions_in(channel).manage_messages, users)):
                await message.unpin()
    
    @react_handler(ContentFilter(foot="^ACTIVE POLL"), "CHANGE")
    async def poll_handler(self, reactions, *, message: discord.Message, emoji,
                           user, event_type, guild: discord.Guild, **_):
        
        counted = {self.bot.user}
        
        async def count_react(rct):
            cnt = 0
            async for memb in rct.users():
                if memb not in counted and has_roles(memb):
                    cnt += 1
                    counted.add(memb)
            return cnt
        
        def has_roles(memb):
            return bool(rls.intersection(set(memb.roles))) if rls else True

        emb = message.embeds[0]
        author = re.match("^ACTIVE POLL by (.*)", emb.footer.text).group(1)
        if event_type == "REACTION_ADD" and str(emoji) == f"\N{CROSS MARK}" and str(user) == author:
            await message.delete()
            return
            
        roles_str = re.match(r"^For (.*)", emb.description).group(1).split(", ")
        if roles_str[0] == "@everyone":
            rls = None
        else:
            rls = set()
            for name_pair in roles_str:
                r_id = int(re.match(r"^.*\((\d*)\)$", name_pair).group(1))
                rls.add(guild.get_role(r_id))
        
        reactions = list(filter((lambda x: str(x.emoji) in EMOJI["DIGITS"]), reactions))
        r_counts = [await count_react(react) for react in reactions]
        total = max(1, sum(r_counts))
        new_emb = self.build_embed(title=emb.title, description=emb.description, footer={"text": emb.footer.text})
        end = 0
        pctg = []
        for field, r_count in zip(emb.fields, r_counts):
            d = r_count/total
            cl = re.search(r"\(Colour: \#([0-9a-fA-F]+)\)$", field.name).group(1)
            col = np.array(Colour(int(cl, 16)).to_rgb())
            pctg.append(d*col)
            nd = end + d
            new_emb.add_field(name=field.name, inline=False, value=f"```{fill_between(end, nd)}```")
            end = nd
        new_emb.colour = Colour.from_rgb(*(int(x) for x in sum(pctg)))
        
        await message.edit(embed=new_emb)
    
    async def handle_event(self, *, message, event_type, emoji, user: discord.User, **kwargs):
        reactions = message.reactions
        if user.id == self.bot.user.id:
            return
        for handler, filt in self.handlers["CHANGE"] + self.handlers[event_type]:
            assert isinstance(filt, Filter)
            if filt.check_msg(message, emoji):
                await handler(filt.filter(reactions), message=message, event_type=event_type,
                              emoji=emoji, user=user, **kwargs)

    @commands.command(name="poll")
    @format_doc
    async def make_poll(self, ctx: commands.Context,
                        option_count: int, colours: Greedy[Colour] = ANTI_RAINBOW,
                        roles: Greedy[discord.Role] = None, *args):
        """Make a poll for people to vote on. At most 10 different options.

        {0}poll 3 red  @​everyone Favourite letter?
          -> new red poll, "Favourite letter?" with options "a", "b" and "c".
        {0}poll 2 up down @​everyone Best direction?
          -> new poll, "Best direction?" with options "up" and "down"."""
        
        if roles is None:
            roles_str = "@everyone"
        else:
            roles_str = ", ".join((f"{rl.name} ({rl.id})" for rl in roles))
        if not (10 >= option_count and len(args) >= option_count > 0):
            raise commands.BadArgument("Incorrect number of options!")
        options = args[:option_count]
        title = " ".join(args[option_count:])
        embed = self.build_embed(title=title, description=f"For {roles_str}",
                                 footer={"text": f"ACTIVE POLL by {ctx.author}"})
        for option, col, emo in zip(options, cycle(colours), EMOJI["DIGITS"][:len(args)]):
            assert isinstance(col, discord.Color)
            embed.add_field(name=f"{emo}. {option} (Colour: {str(col)})",
                            value=f"```{fill_between(0, 0)}```", inline=False)
        msg = await ctx.send(embed=embed)
        await react_for(msg, f"\N{CROSS MARK}", *EMOJI["DIGITS"][:option_count])

    async def unpack_payload(self, payload):
        message_id = payload.message_id
        user_id = payload.user_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
        emoji = payload.emoji
        channel = self.bot.get_channel(channel_id)
        guild = self.bot.get_guild(guild_id)
        user = self.bot.get_user(user_id)
        try:
            member = payload.member
        except AttributeError:
            if guild:
                member = guild.get_member(user_id)
            else:
                member = None
        message = await channel.fetch_message(message_id)
        return {"message_id": message_id,
                "user_id": user_id,
                "channel_id": channel_id,
                "guild_id": guild_id,
                "emoji": emoji,
                "member": member,
                "channel": channel,
                "guild": guild,
                "user": user,
                "message": message}
