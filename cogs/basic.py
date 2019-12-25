import asyncio
from urllib.parse import quote_plus
from discord.ext import commands
from cogs.base import CogBase
import time

PING_CPU_PASSES = 20
MAX_ALERT = 1.00
MIN_IDEAL = 0.25


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
            f"   PING: {total_ping * 1_000: .2f}ms",
            f"+ GATEW: #{self.make_progress_bar(heartbeat_latency_pct)}# {heartbeat_latency * 1_000: .2f}ms",
            f"-  REST: #{self.make_progress_bar(message_send_time_pct)}# {message_send_time * 1_000: .2f}ms",
            f"   LOOP: {total_loop * 1_000_000: .2f}µs",
            f"+ STACK: #{self.make_progress_bar(function_latency_pct)}# {function_latency * 1_000_000: .2f}µs",
            f"- CALLB: #{self.make_progress_bar(sync_latency_pct)}# {sync_latency * 1_000_000: .2f}µs",
            f"+   AIO: #{self.make_progress_bar(async_latency_pct)}# {async_latency * 1_000_000: .2f}µs",
            "```",
        )
        
        severity = (total_ping - MIN_IDEAL)/(MAX_ALERT - MIN_IDEAL)

        if severity >= 1:
            severity_col = 0xff0000
        elif severity <= 0:
            severity_col = 0x00ff00
        elif severity > 0.5:
            sv = (severity - 0.5) * 2
            severity_col = sv * 0xff0000
            severity_col += (1-sv) * 0xffff00
        else:
            sv = severity * 2
            severity_col = sv * 0xffff00
            severity_col += (1-sv) * 0x00ff00
        
        severity_col = round(severity_col)
        
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
