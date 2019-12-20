import asyncio
import random
import time
from discord.ext import commands
from botconstants import EMOJI, PREFIX_RAW
from cogs.base import CogBase


class GamesCog(CogBase):
    """Fun games!"""

    COLOUR = 0xFFFFFF

    class Snake:
        def __init__(self):
            self.frameTime = 1
            self.startSize = 4
            self.snake = [(2, 5), (3, 5), (4, 5), (5, 5)]
            self.x_vect = 1
            self.y_vect = 0
            self.apple = (5, 5)
            self.bSize = 11
            self.running = True
            self.plant_apple()

        def update(self):
            if not self.running:
                return
            self.snake.append((self.snake[-1][0] + self.x_vect, self.snake[-1][1] + self.y_vect))
            snake = self.snake[-1]
            if (self.snake[-1] in self.snake[:-1] or
                    snake[0] >= self.bSize or
                    snake[1] >= self.bSize or
                    snake[0] < 0 or
                    snake[1] < 0):
                self.running = False
                self.snake.pop(0)
                return
            if self.apple not in self.snake:
                self.snake.pop(0)
            else:
                self.plant_apple()

        def plant_apple(self):
            while self.apple in self.snake:
                self.apple = (random.randint(0, self.bSize - 1), random.randint(0, self.bSize - 1))

        @property
        def render_string(self):
            render_string = ""
            for i in range(self.bSize + 2):
                render_string += "$ "
            render_string += "\n"
            for y in range(self.bSize):
                render_string += "$ "
                for x in range(self.bSize):
                    render_string += "@ " if self.apple == (x, y) else ("# " if (x, y) in self.snake else "  ")
                render_string += "$\n"
            for i in range(self.bSize + 2):
                render_string += "$ "
            return render_string

    @commands.command(name="snake")
    async def play_snake(self, ctx, magic="no"):
        """Play snake.

        Communist edition."""
        reactants = EMOJI["ARROWS"]["ARRAY"]
        snake_game = self.Snake()

        if magic == "communist":
            snake_game.apple = (-1, -1)

        bot_msg = await ctx.send("```{}```".format(snake_game.render_string))
        for reactant in reactants:
            await bot_msg.add_reaction(reactant)

        msg = await ctx.fetch_message(bot_msg.id)
        while snake_game.running:
            timer = time.time()
            commandments = {0: 0, 1: 0, 2: 0, 3: 0}
            for reaction in msg.reactions:
                async for user in reaction.users():
                    if user != self.bot.user:
                        await reaction.remove(user)
                        if reaction.emoji in reactants:
                            commandments[reactants.index(reaction.emoji)] += 1
            vote = max(commandments.keys(), key=lambda x: commandments[x])
            if commandments[vote] > 0:
                snake_game.x_vect, snake_game.y_vect = ((0, -1), (0, 1), (-1, 0), (1, 0))[vote]
            snake_game.update()
            game_s = "```{}```".format(snake_game.render_string)
            await msg.edit(content=game_s)
            await asyncio.sleep(timer + 1 - time.time())

        e = self._make_embed(title="Game Over!",
                             description="Ended game with length: " + str(len(snake_game.snake)),
                             colour=0x3232ef,
                             footer={"text": "{}snake to play again".format(PREFIX_RAW)})

        await msg.clear_reactions()
        await msg.edit(content="", embed=e)
