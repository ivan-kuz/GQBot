import inspect
import asyncio
import discord
from cogs.base import CogBase
from utils.filters import *
from utils.botconstants import VOTING_CHANNELS, PIN_REACTIONS_MIN, POLL_BUFF, POLL_CHAN


def react_handler(filt, watch):
    def wrapper(coro):
        assert asyncio.iscoroutinefunction(coro), "Handler must be a coroutine function"
        setattr(coro, "__react_handler_for__", (filt, watch))
        return coro
    return wrapper


def is_handler(obj):
    try:
        obj.__react_handler_for__
        return True
    except AttributeError:
        return False


class VotingCog(CogBase, name="Voting"):
    """Role and permission managing commands."""

    COLOUR = 0x008888
    
    hidden = True
    
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__(bot)
        
        self.handlers = {"CHANGE": [],
                         "REACTION_ADD": [],
                         "REACTION_REMOVE": []}
        for _, handler in inspect.getmembers(self, is_handler):
            filt, add_to = handler.__react_handler_for__
            self.handlers[add_to].append((handler, filt))
        
        self.poll_chan = None
        self.poll_msg_id = POLL_BUFF
        self.polls = None
        self.dirty = True
    
    async def get_polls(self):
        if not self.dirty:
            return
        if self.poll_msg_id is None:
            msg = await self.poll_chan.send("ACTIVE POLLS")
            self.poll_msg_id = msg.id
            with open("config/poll_msg.id", "w") as fl:
                fl.write(str(self.poll_msg_id))
        else:
            msg = await self.poll_chan.fetch_message(self.poll_msg_id)
        
        pols = msg.content.split("\n")[1:]
        self.polls = [tuple(x.split()) for x in pols]
    
    @staticmethod
    async def set_vote(message):
        if not message.author.bot:
            await message.add_reaction(f"\N{THUMBS UP SIGN}")
            await message.add_reaction(f"\N{THUMBS DOWN SIGN}")
    
    @CogBase.listener()
    async def on_ready(self):
        """Set votes for messages sent when bot was offline."""
        self.poll_chan = self.bot.get_channel(POLL_CHAN)
        
        for c_id in VOTING_CHANNELS:
            channel = self.bot.get_channel(c_id)
            async for msg in channel.history():
                if any(map(lambda x: x.me, msg.reactions)):
                    break
                await self.set_vote(msg)
        
        await self.get_polls()
    
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
    
    @react_handler((f"\N{PUSHPIN}",), "CHANGE")
    async def pin_handler(self, reactions, *, message, channel, event_type, **_):
        if event_type == "REACTION_ADD" and not message.pinned:
            reaction = reactions[0]
            users = await reaction.users().flatten()
            if len(users) >= PIN_REACTIONS_MIN or \
               any(map(lambda x: x.permissions_in(channel).manage_messages, users)):
                await message.pin()
            async for msg in channel.history():
                if msg.type == discord.MessageType.pins_add:
                    await msg.delete()
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
    
    @react_handler(OmniCont(), "CHANGE")
    async def poll_handler(self, reactions, *, message, emoji, **kwargs):
        reactions = list(filter(lambda x: x.me, reactions))
        print("hi")
    
    async def handle_event(self, *, message, event_type, emoji, **kwargs):
        reactions = message.reactions
        for filt, w_l, handler in self.handlers["CHANGE"] + self.handlers[event_type]:
            filtered = filt(reactions)
            if str(emoji) in w_l:
                await handler(filtered, message=message, event_type=event_type,
                              emoji=emoji, **kwargs)
    
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
