from discord.ext import commands
from cogs.base import CogBase
from utils import format_doc, PREFIX_RAW


class HelpCog(CogBase, name="Help"):
    """Help command."""

    COLOUR = 0x000000

    def __init__(self, bot: commands.bot):
        super().__init__(bot)
        self.bot.remove_command("help")

    @commands.command()
    @format_doc
    async def help(self, ctx, *args):
        """The command you are using right now.

        {0}help --> list all cogs, and their commands
        {0}help <cog name> --> get detailed help
        {0}help <command> --> detailed help on the command and its usage"""
        if not args:  # If there are no arguments, list all available commands.
            for cog in self.bot.cogs:
                a_cog = self.bot.get_cog(cog)
                if a_cog.hidden:
                    continue
                await self.get_help_on(ctx, a_cog, cog == self.qualified_name)
        # If there are arguments, find what is being referenced.
        elif " ".join(args) in self.bot.cogs:  # Looks like they are referencing a cog, give detailed help on it.
            await self.get_help_on(ctx, self.bot.cogs[" ".join(args)], True)
        else:
            c_super = self.bot
            for arg in args:
                unchanged = True
                try:
                    c_super.commands
                except AttributeError:
                    break
                for child in c_super.commands:
                    if arg == child.name or arg in child.aliases:
                        c_super = child
                        unchanged = False
                if unchanged:
                    raise commands.CommandNotFound(" ".join(args))
            await self.get_help_on(ctx, c_super, True)

    @staticmethod
    async def get_help_on(ctx, item, detailed=False):
        if isinstance(item, CogBase):
            sub_commands = [{"name": cmd,
                             "value": cmd.help if detailed else cmd.help.split("\n")[0],
                             "inline": False}
                            for cmd in item.get_commands()]
            embed = item.build_embed(*sub_commands, title=item.qualified_name, description=item.description)
        elif isinstance(item, commands.Group):
            sub_commands = [{"name": cmd,
                             "value": cmd.help if detailed else cmd.help.split("\n")[0],
                             "inline": False}
                            for cmd in item.commands]
            embed = item.cog.build_embed(*sub_commands, title=item.qualified_name, description=item.help)
        elif isinstance(item, commands.Command):
            desc = """{prefix}{name}{aliases} {signature}
            
            {help}""".format(prefix=PREFIX_RAW,
                             name=item.qualified_name,
                             aliases="[, {}]".format(", ".join(item.aliases)) if item.aliases else "",
                             signature=item.signature,
                             help=item.help)
            embed = item.cog.build_embed(title=item.qualified_name, description=desc)
        else:
            raise commands.CommandNotFound(str(item))
        await ctx.send(embed=embed)
