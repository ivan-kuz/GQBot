from discord.ext import commands
import discord
from typing import Dict, Union

Field = Dict[str, Union[str, bool]]
Footer = Dict[str, str]
Author = Dict[str, str]


class CogBase(commands.Cog):
    """Base cog. Other cogs implement this."""

    COLOUR = 0xFF0000

    hidden = False

    @property
    def colour(self) -> int:
        return self.COLOUR

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    def build_embed(self,
                    *fields: Field,
                    footer: Footer = None,
                    colour: int = None,
                    image: str = None,
                    thumbnail: str = None,
                    author: Author = None,
                    **kwargs) -> discord.Embed:

        if colour is None:  # Set the colour to the Cog's colour if none is given.
            colour = self.colour

        embed = discord.Embed(colour=colour, **kwargs)  # Initialise embed with given keyword arguments.

        for field in fields:
            embed.add_field(**field)

        if image is not None:
            embed.set_image(url=image)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if footer is not None:
            embed.set_footer(**footer)
        if author is not None:
            embed.set_author(**author)

        return embed

    async def _send_simple(self, ctx: commands.Context, text: str, title: str = None) -> None:
        await ctx.send(embed=self.build_embed(title=self._get_embed_title(ctx) if title is None else title,
                                              description=text))

    async def _send_advanced(self, ctx, text="", *args, **kwargs):
        e = self.build_embed(*args, **kwargs)
        await ctx.send(text, embed=e)

    # method may need to be dynamic for child classes
    # noinspection PyMethodMayBeStatic
    def _get_embed_title(self, ctx: commands.Context):
        return ctx.invoked_with
