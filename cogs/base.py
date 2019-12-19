from discord.ext import commands


class CogBase(commands.Cog):
    """Base cog. Other cogs implement this."""

    COLOUR = 0xFF0000

    @property
    def colour(self):
        return self.COLOUR

    def __init__(self, bot):
        self.bot = bot
