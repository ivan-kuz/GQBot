from discord.ext import commands
from utils import BarHelper
from utils.botconstants import PREFIX, TOKEN
import cogs

print("Finished imports!")

bot = commands.Bot(command_prefix=PREFIX)

print("Loading cogs...")
_bh = BarHelper(cogs.COG_COUNT)
_bh.print()
for cog in cogs.COGS:
    _bh.progress(end=f" {cog.__name__}\n")
    bot.add_cog(cog(bot))
print("Loaded cogs!")

@bot.event
async def on_ready():
    print("...GQBot is online!\nHail the Fathers!")


@bot.event
async def on_connect():
    print("Connected...")


@bot.event
async def on_disconnect():
    print("Lost connection.")


bot.run(TOKEN)
