from discord.ext import commands
import random
from pattern.text.en import conjugate
from cogs.base import CogBase
from utils import sentence_case, list_values, format_doc


class ChanceCog(CogBase, name="Chance"):
    """Plays dice, unlike God."""

    @property
    def colour(self):
        return random.randint(0, 0xFFFFFF)  # The color will be random each time it is requested.

    @commands.command(aliases=["toss", "throw"])
    async def flip(self, ctx: commands.Context, action, *extra_flavour: str):
        """Flips a coin."""
        # Ensure that the verb used is the one used to invoke the command.
        if not action:
            action = ctx.invoked_with
        while True:
            try:
                verb = conjugate(action, "VBG")  # Conjugate to be a present participle.
                if extra_flavour:
                    verb += " "+" ".join(extra_flavour)
                break
            except RuntimeError:  # conjugate seems to have problems running the first time.
                pass
        verb = sentence_case(verb)
        await self._send_simple(ctx, "It landed {}!".format(random.choice(("heads", "tails"))),
                                "{} coin... ".format(verb))

    @commands.command(aliases=["choose", "spin"])
    @format_doc
    async def roll(self, ctx, *args):
        """Rolls dice, or picks a choice at random.

        {0}roll --> rolls a single 6-sided die
        {0}roll x --> rolls a single x-sided die
        {0}roll x y --> rolls y x-sided dice
        {0}roll/choose/spin a b c d ... --> outputs one of the choices at random

        If any values for the second and third commands are invalid, they default to x=6; y=1."""

        invocation = ctx.invoked_with

        sides = None
        result = ""
        flavour = ""
        if invocation == "roll":
            dice = 1
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
            if sides is not None:
                result = 0
                for i in range(dice):
                    result += random.randint(1, sides)
                result = str(result)
                flavour = str(sides) + " sided di"
                if dice == 1:
                    flavour += "e"
                else:
                    flavour += "ce, " + str(dice) + " of them"
        if sides is None:
            if len(args) == 0:
                result = "nothing. You can't {} from 0 choices.".format(invocation)
            else:
                result = '"'+random.choice(args)+'"'
            if len(args) > 3 or len(args) < 1:
                flavour = "between "+str(len(args))+" choices. "
            else:
                flavour = "between " + list_values(['"{}"'.format(x) for x in args])
        while True:
            try:
                verb = conjugate(invocation, "VBG")  # Conjugate to be a present participle.
                break
            except RuntimeError:  # conjugate seems to have problems running the first time.
                pass
        await self._send_simple(ctx, "Landed: " + result, "{} {}.".format(sentence_case(verb), flavour))
