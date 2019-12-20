from discord.ext import commands
from cogs.base import CogBase
from collections import OrderedDict


class HelpCog(CogBase, name="Help"):
    """Help command."""

    COLOUR = 0x000000

    def __init__(self, bot: commands.bot):
        super().__init__(bot)
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, *args):
        """The command you are using right now."""
        if not args:
            for cog in self.bot.cogs:
                await self.get_help_on(ctx, self.bot.get_cog(cog))

    @staticmethod
    async def get_help_on(ctx, item):
        if isinstance(item, CogBase):
            sub_commands = ({"name": cmd, "value": cmd.help.split("/n")[0], "inline": False} for cmd in item.get_commands())
            embed = item._make_embed(*sub_commands, title=item.qualified_name, description=item.description)
            await ctx.send(embed=embed)
