import asyncio
from urllib.parse import quote_plus
from discord.ext import commands
from cogs.base import CogBase


class BasicCog(CogBase, name="Basic"):
    """Basic commands, such as links."""

    COLOUR = 0x0000FF

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await self._send_simple(ctx, "Pong!")

    @commands.command()
    async def hail(self, ctx):
        """Hails the fathers."""
        await self._send_simple(ctx, "Hail the fathers!")

    @commands.command()
    @commands.has_permissions(mention_everyone=True)
    @commands.cooldown(1, 3600)
    async def spam100(self, ctx):
        """Spam pings everyone 100 times."""
        for i in range(100):
            await self._send_simple(ctx, "@everyone bow down to the GQEmpire")
            await asyncio.sleep(2)

    @commands.command()
    async def romatime(self, ctx):
        """Link to romatime.gq"""
        await self._send_simple(ctx, "http://romatime.gq")
        await self._send_simple(ctx, "The most recent episode is: " + "https://www.youtube.com/watch?v=pUcxS8Cnyfg")

    @commands.command()
    async def aquaesulis(self, ctx):
        """Link to aquaesulis.gq"""
        await self._send_simple(ctx, "http://aquaesulis.gq")

    @commands.command()
    async def tiffinbbc(self, ctx):
        """Link to tiffinbbc.gq"""
        await self._send_simple(ctx, "http://tiffinBBC.gq")
        await self._send_simple(ctx, "WARNING! Formatting might look really weird on big screens!")

    @commands.command()
    async def github(self, ctx):
        """Link to GQBot's Github repo."""
        await self._send_simple(ctx, "https://github.com/ivan-kuz/GQBot/")
        await self._send_simple(ctx, "This is the github repo for the GQBot." +
                                     "If you're an avid coder, feel free to contribute to this wonderful bot!")

    @commands.command()
    async def wiki(self, ctx):
        """Link to GQBot's Github wiki."""
        await self._send_simple(ctx, "https://github.com/ivan-kuz/GQBot/wiki")
        await self._send_simple(ctx, "This is the link to the wiki for the GQBot." +
                                     "If you need some help - you will definitely find it on there!")

    @commands.command()
    async def quests(self, ctx):
        """Link to quests.gq"""
        await self._send_simple(ctx, "Press 'Run' to play your first quest!")
        await self._send_simple(ctx, "http://quests.aquaesulis.gq")

    @commands.command()
    async def gqempire(self, ctx):
        """Links to GQEmpire.gq"""
        await self._send_simple(ctx, "http://GQEmpire.gq")
        await self._send_simple(ctx, "This is your main site! Feel free to make it your homepage :)")

    @commands.command()
    async def lmgtfy(self, ctx, *query: str):
        """Let me Google that for you.

        Enter a query to search for that, or leave blank to search for the last message."""
        if not query:  # "LMGTFY" the previous message.
            flag = False
            async for msg in ctx.history():
                if flag:
                    query = msg.content
                    break
                elif msg.id == ctx.message.id:
                    flag = True

        await self._send_simple(ctx, "https://lmgtfy.com/?q={}".format(quote_plus(query)))
