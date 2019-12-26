import asyncio
from urllib.parse import quote_plus
from discord.ext import commands
from discord import Colour, Embed
from cogs.base import CogBase
import time
import numpy as np

PING_CPU_PASSES = 20
MAX_ALERT = 1.00
MIN_IDEAL = 0.25

HIGH = np.array((255, 0, 0))
MID = np.array((255, 165, 0))
LOW = np.array((0, 255, 0))
            
def link_command(link: str, *, name: str = None, **d_kwargs):
    def decorator(funct, name):
        async def send_link(self, ctx):  # Cog loaded commands need a self parameter or smth.
            nonlocal _e_dict
            if _e_dict is None:
                _e_dict = BasicCog(None).build_embed(url=link, thumbnail=link, title=link).to_dict()
            embed = _e_dict
            await funct(self, ctx, embed)
        _e_dict = None
        send_link.__doc__ = funct.__doc__
        if name is None:
            name = funct.__name__
        send_link = commands.command(name=name, **d_kwargs)(send_link)
        return send_link
    return lambda x: decorator(x, name)



class BasicCog(CogBase, name="Basic"):
    """Basic commands, such as links."""

    COLOUR = 0x0000FF

    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """Pong!"""
        # Calculate the message-send time. This is the time taken to the response.
        message_send_time = time.perf_counter()

        pong_or_ping = "PING" if ctx.invoked_with == "pong" else "PONG"

        msg = await ctx.send(f"{pong_or_ping}...")
        message_send_time = time.perf_counter() - message_send_time

        heartbeat_latency = ctx.bot.latency

        # Calculate the event loop latency. This is a good representation of how
        # slow the loop is running. We spin the processor up first on the
        # current core to get an accurate measurement of speed when the CPU core
        # is under full load.

        # Time to do a round trip on the event loop, and time to callback.
        end_sync, end_async, end_fn = 0, 0, 0
        sync_latency, async_latency, function_latency = 0, 0, 0

        # Used to measure latency of a task.
        async def coro():
            """
            Empty coroutine that is used to determine the rough waiting time
            in the event loop.
            """
            pass

        # Measures time between the task starting and the callback being hit.
        def sync_callback(_):
            """
            Callback invoked once a coroutine has been ensured as a future.
            This measures the rough time needed to invoke a callback.
            """
            nonlocal end_sync
            end_sync = time.perf_counter()

        def fn_callback():
            """
            Makes a guesstimate on how long a function takes to invoke relatively.
            """
            nonlocal end_fn
            end_fn = time.perf_counter()

        for _ in range(0, 200):
            pass  # Dummy work to spin the CPU up

        for i in range(0, PING_CPU_PASSES):
            start = time.perf_counter()
            async_call = ctx.bot.loop.create_task(coro())
            async_call.add_done_callback(sync_callback)
            await async_call
            end_async = time.perf_counter()

            sync_latency += end_sync - start
            async_latency += end_async - start

            start = time.perf_counter()
            fn_callback()
            function_latency += end_fn - start

        function_latency /= PING_CPU_PASSES
        async_latency /= PING_CPU_PASSES
        sync_latency /= PING_CPU_PASSES

        # We match the latencies with respect to the total time taken out of all
        # of them
        total_ping = 1.05 * (message_send_time + heartbeat_latency)
        total_loop = 1.05 * (async_latency + sync_latency + function_latency)

        message_send_time_pct = message_send_time * 100 / total_ping
        heartbeat_latency_pct = heartbeat_latency * 100 / total_ping
        async_latency_pct = async_latency * 100 / total_loop
        sync_latency_pct = sync_latency * 100 / total_loop
        function_latency_pct = function_latency * 100 / total_loop

        joiner = lambda *a: "\n".join(a)

        pong = joiner(
            "```diff",
            f"   PING: {total_ping * 1_000 *20/21: .2f}ms",
            f"+ GATEW: #{self.make_progress_bar(heartbeat_latency_pct)}# {heartbeat_latency * 1_000: .2f}ms",
            f"-  REST: #{self.make_progress_bar(message_send_time_pct)}# {message_send_time * 1_000: .2f}ms",
            f"   LOOP: {total_loop * 1_000_000 *20/21: .2f}µs",
            f"+ STACK: #{self.make_progress_bar(function_latency_pct)}# {function_latency * 1_000_000: .2f}µs",
            f"- CALLB: #{self.make_progress_bar(sync_latency_pct)}# {sync_latency * 1_000_000: .2f}µs",
            f"+   AIO: #{self.make_progress_bar(async_latency_pct)}# {async_latency * 1_000_000: .2f}µs",
            "```",
        )
        
        severity = (total_ping - MIN_IDEAL)/(MAX_ALERT - MIN_IDEAL)

        if severity >= 1:
            severity_col = HIGH
        elif severity <= 0:
            severity_col = LOW
        elif severity > 0.5:
            sv = (severity - 0.5) * 2
            severity_col = sv * HIGH
            severity_col += (1-sv) * MID
        else:
            sv = severity * 2
            severity_col = sv * MID
            severity_col += (1-sv) * LOW
        
        r, g, b = (int(i) for i in severity_col)
        
        severity_col = Colour.from_rgb(r, g, b)
        
        embed = self.build_embed(title=pong_or_ping, description=pong, colour=severity_col)

        await msg.edit(content="", embed=embed)

    @staticmethod
    def make_progress_bar(percent):
        full = "\N{FULL BLOCK}"
        empty = " "
        percent_per_block = 5

        return "".join(full if i < percent else empty for i in range(0, 100, percent_per_block))

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

    @link_command("http://romatime.gq")
    async def romatime(self, ctx, embed):
        """Link to romatime.gq"""
        embed = Embed(**embed, description="The most recent episode is:\n"+
                                           "https://www.youtube.com/watch?v=pUcxS8Cnyfg")
        await ctx.send(embed=embed)

    @link_command("http://aquaesulis.gq")
    async def aquaesulis(self, ctx, embed):
        """Link to aquaesulis.gq"""
        await ctx.send(embed=Embed(**embed, description="Learn all about Aquae Sulis!"))

    @link_command("http://tiffinBBC.gq")
    async def tiffinbbc(self, ctx, embed):
        """Link to tiffinbbc.gq"""
        embed = Embed(**embed, description="WARNING! Formatting might look really weird on big screens!")
        await ctx.send(embed=embed)

    @link_command("https://github.com/ivan-kuz/GQBot/")
    async def github(self, ctx, embed):
        """Link to GQBot's Github repo."""
        embed = Embed(**embed, description="This is the github repo for the GQBot." + \
                                  "If you're an avid coder, feel free to " + \
                                  "contribute to this wonderful bot!")
        await ctx.send(embed=embed)

    @link_command("https://github.com/ivan-kuz/GQBot/wiki")
    async def wiki(self, ctx, embed):
        """Link to GQBot's Github wiki."""
        embed = Embed(**embed, description="This is the link to the wiki for the GQBot." + \
                                  "If you need some help - you will definitely find it on there!")
        await ctx.send(embed=embed)

    @link_command("http://quests.aquaesulis.gq")
    async def quests(self, ctx, embed):
        """Link to quests.gq"""
        await ctx.send(embed=Embed(**embed, description="Press 'Run' to play your first quest!"))

    @link_command("http://GQEmpire.gq")
    async def gqempire(self, ctx, embed):
        """Links to GQEmpire.gq"""
        await ctx.send(embed=Embed(**embed, description="This is your main site! Feel free to make it your homepage :)"))

    @commands.command()
    async def lmgtfy(self, ctx, *query: str):
        """Let me Google that for you.

        Enter a query to search for that, or leave blank to search for the last message."""
        if not query:  # "LMGTFY" the previous message.
            flag = False
            async for msg in ctx.history():
                if flag:
                    if not msg.content:
                        continue
                    query = msg.content
                    break
                elif msg.id == ctx.message.id:
                    flag = True

        await self._send_advanced(ctx, title="Let me Google that for you!",
                                  description=query,
                                  url="https://lmgtfy.com/?q={}".format(quote_plus(query)))
