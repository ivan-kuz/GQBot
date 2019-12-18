import asyncio
from urllib.parse import quote_plus

from discord.ext import commands


class BasicCog(commands.Cog):
    """Basic commands, such as links."""

    COLOUR = 0x0000FF

    @staticmethod
    def get_colour():
        return BasicCog.COLOUR

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send("Pong!")

    @commands.command()
    async def hail(self, ctx):
        """Hails the fathers."""
        await ctx.send("Hail the fathers!")

    @commands.command()
    @commands.has_permissions(mention_everyone=True)
    @commands.cooldown(1, 3600)
    async def spam100(self, ctx):
        """Spam pings everyone 100 times."""
        for i in range(100):
            await ctx.send("@everyone bow down to the GQEmpire")
            await asyncio.sleep(2)

    @commands.command()
    async def romatime(self, ctx):
        """Link to romatime.gq"""
        await ctx.send("http://romatime.gq")
        await ctx.send("The most recent episode is: " + "https://www.youtube.com/watch?v=pUcxS8Cnyfg")

    @commands.command()
    async def aquaesulis(self, ctx):
        """Link to aquaesulis.gq"""
        await ctx.send("http://aquaesulis.gq")

    @commands.command()
    async def tiffinbbc(self, ctx):
        """Link to tiffinbbc.gq"""
        await ctx.send("http://tiffinBBC.gq")
        await ctx.send("WARNING! Formatting might look really weird on big screens!")

    @commands.command()
    async def github(self, ctx):
        """Link to GQBot's Github repo."""
        await ctx.send("https://github.com/ivan-kuz/GQBot/")
        await ctx.send("This is the github repo for the GQBot." +
                       "If you're an avid coder, feel free to contribute to this wonderful bot!")

    @commands.command()
    async def wiki(self, ctx):
        """Link to GQBot's Github wiki."""
        await ctx.send("https://github.com/ivan-kuz/GQBot/wiki")
        await ctx.send("This is the link to the wiki for the GQBot." +
                       "If you need some help - you will definitely find it on there!")

    @commands.command()
    async def quests(self, ctx):
        """Link to quests.gq"""
        await ctx.send("Press 'Run' to play your first quest!")
        await ctx.send("http://quests.aquaesulis.gq")

    @commands.command()
    async def gqempire(self, ctx):
        """Links to GQEmpire.gq"""
        await ctx.send("http://GQEmpire.gq")
        await ctx.send("This is your main site! Feel free to make it your homepage :)")

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

        await ctx.send("https://lmgtfy.com/?q={}".format(quote_plus(query)))
