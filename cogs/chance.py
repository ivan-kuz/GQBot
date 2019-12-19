from discord.ext import commands
import random
from botconstants import format_doc
from cogs.base import CogBase


class ChanceCog(CogBase):
    """Plays dice, unlike God."""

    @property
    def colour(self):
        return random.randint(0, 0xFFFFFF)  # The color will be random each time it is requested.

    @commands.command()
    async def toss(self, ctx):
        """Tosses a coin."""
        await ctx.send("Tossing coin... It landed " + random.choice(("heads", "tails"))+"!")

    @commands.command()
    async def flip(self, ctx):
        """Flips a coin."""
        await ctx.send("Flipping coin... It landed " + random.choice(("heads", "tails"))+"!")

    @commands.command()
    @format_doc
    async def roll(self, ctx, *args):
        """Rolls dice, or picks a choice at random.

        {0}roll --> rolls a single 6-sided die
        {0}roll x --> rolls a single x-sided die
        {0}roll x y --> rolls y x-sided dice
        {0}roll a b c d ... --> outputs one of the choices at random

        If any values for the second and third commands are invalid, they default to x=6; y=1."""
        dice = 1
        sides = None
        if len(args) == 0:
            sides = 6
        elif len(args) == 1:
            try:
                sides = int(args[0])
                if sides < 1:
                    sides = 6
            except ValueError:
                sides = 6
        elif len(args) == 2:
            try:
                sides = int(args[0])
                dice = int(args[1])
                if sides < 1:
                    sides = 6
                if dice < 1:
                    dice = 1
            except ValueError:
                sides = None
        if sides is None:
            result = '"'+random.choice(args)+'"'
            flavour = "between "+str(len(args))+" choices. "
        else:
            result = 0
            for i in range(dice):
                result += random.randint(1, sides)
            result = str(result)
            flavour = str(sides) + " sided di"
            if dice == 1:
                flavour += "e. "
            else:
                flavour += "ce, "+str(dice)+" of them. "
        await ctx.send("Rolling " + flavour + "Landed: " + result)
