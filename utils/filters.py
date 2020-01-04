import re

from discord import Reaction, Message, PartialEmoji, Emoji
from typing import List, Union

EmojiType = Union[PartialEmoji, Emoji, str]


class Filter:
    """Always True."""
    def check_msg(self, message: Message, emoji: EmojiType) -> bool:
        return True
    
    def __call__(self, reaction: Reaction) -> bool:
        return True

    def filter(self, reactions: List[Reaction]) -> List[Reaction]:
        return list(filter(self, reactions))


class Default(Filter):
    def __call__(self, reaction: Reaction) -> bool:
        return reaction.me


class FilterFor(Filter):
    def __init__(self, *emoji: EmojiType):
        self.emoji = emoji

    def check_msg(self, message: Message, emoji: EmojiType) -> bool:
        return (emoji in self.emoji) or (str(emoji) in self.emoji)

    def __call__(self, reaction: Reaction) -> bool:
        return reaction.emoji in self.emoji


CONT_ALL = type("ContAll", (object,), {"__contains__": lambda _, __: True, "add": lambda _, a: set(a)})()


class ChannelMsgFilter(Default):
    def __init__(self, *, channels: List[int] = CONT_ALL, messages: List[int] = CONT_ALL, guilds: List[int] = CONT_ALL):
        self.channels = channels
        self.messages = messages
        self.guilds = guilds

    def check_msg(self, message: Message, emoji: EmojiType) -> bool:
        return message.id in self.messages and message.channel.id in self.channels and message.guild.id in self.guilds


class ContentFilter(Default):
    def __init__(self, *, content=None, title=None, desc=None, foot=None):
        self.content = re.compile(content) if content else None
        self.title = re.compile(title) if title else None
        self.desc = re.compile(desc) if desc else None
        self.foot = re.compile(foot) if foot else None
        self.check_embed = bool(title or desc or foot)

    def check_msg(self, message: Message, emoji: EmojiType) -> bool:
        if self.content is not None:
            if not self.content.match(message.content):
                return False
        if self.check_embed:
            if not message.embeds:
                return False
            emb = message.embeds[0]
            if self.title is not None:
                if not self.title.match(emb.title):
                    return False
            if self.desc is not None:
                if not self.desc.match(emb.description):
                    return False
            if self.foot is not None:
                if not self.foot.match(emb.footer.text):
                    return False
        return True


class FiltUnion(Filter):
    def __init__(self, collapse: Union[all, any] = all, *filters):
        self.filters = filters
        self.collapse = collapse

    def check_msg(self, *args, **kwargs) -> bool:
        return self.collapse((filt.check_message(*args, **kwargs) for filt in self.filters))

    def __call__(self, *args, **kwargs) -> bool:
        return self.collapse((filt(*args, **kwargs) for filt in self.filters))

    def filter(self, *args, **kwargs) -> List[Reaction]:
        all_filtered = (set(filt.filter(*args, **kwargs)) for filt in self.filters)
        call = set.union if self.collapse == any else set.intersection
        return list(call(*all_filtered))
