import asyncio
import inspect
import uuid
import discord
from discord.ext import commands
from cogs.base import CogBase


def mark_as_handler(ex_type, *ex_types):
    def decorator(func):
        assert asyncio.iscoroutinefunction(func), "Handler must be a coroutine function"
        setattr(func, "__error_handler_for__", [ex_type, *ex_types])
        return func
    return decorator


def is_handler(obj):
    try:
        return all(issubclass(cls, Exception) for cls in obj.__error_handler_for__)
    except AttributeError:
        return False


# These are exception types we can safely print out to the user in a message with no checking.
MANAGED_EXCEPIONS = [
    commands.NotOwner,
    commands.MissingRequiredArgument,
    commands.BadArgument,
    commands.BotMissingPermissions,
    commands.MissingPermissions,
    commands.NoPrivateMessage,
    commands.TooManyArguments,
    discord.Forbidden,
    discord.NotFound,
]


class ErrorHandlerCog(CogBase):
    """Handles exceptions."""
    
    COLOUR = 0xc80606
    
    hidden = True
    
    def __init__(self, bot):
        super().__init__(bot)
        self.handlers = {}
        for _, handler in inspect.getmembers(self, is_handler):
            for ex_t in handler.__error_handler_for__:
                self.handlers[ex_t] = handler

    @CogBase.listener()
    async def on_command_error(self, ctx, error):
        print(f"Handling exception: {error}")

        cause = error.__cause__ \
                if error.__cause__ and \
                   not isinstance(error, commands.BadArgument) \
                else error

        for klass in type(cause).mro():
            c = klass in self.handlers
            if c:
                return await self.handlers[klass](ctx, cause)

    @mark_as_handler(commands.CommandNotFound)
    async def on_command_not_found(self, ctx, error):
        command = ctx.message.content[len(ctx.prefix) :].strip()
        await ctx.message.add_reaction("\N{BLACK QUESTION MARK ORNAMENT}")

    @mark_as_handler(commands.DisabledCommand, commands.CheckFailure)
    async def on_command_disabled(self, ctx, error):
        await ctx.message.add_reaction("\N{NO ENTRY SIGN}")

    @mark_as_handler(commands.CommandOnCooldown)
    async def on_command_on_cooldown(self, ctx, error):
        reaction = "\N{SNOWFLAKE}\N{VARIATION SELECTOR-16}"
        asyncio.create_task(ctx.message.add_reaction(reaction))
        await asyncio.sleep(error.retry_after)
        try:
            await ctx.message.remove_reaction(reaction, ctx.bot.user)
        except discord.NotFound:
            pass

    @mark_as_handler(NotImplementedError)
    async def on_not_implemented_error(self, ctx, error):
        await ctx.message.add_reaction("\N{CONSTRUCTION SIGN}")

    @mark_as_handler(*MANAGED_EXCEPIONS)
    async def on_managed_exception(self, ctx, error):
        message = str(error).strip()
        if message:
            await self._send_simple(ctx, message, type(error).__name__)

    @mark_as_handler(Exception)
    async def on_unhandled_exception(self, ctx, error):
        ref = uuid.uuid4()
        print("Unhandled exception! UUID: {}\n{}".format(ref, error))
        await self._send_advanced(ctx, title="Uh oh, something " +
                                  "unexpected went wrong!",
                                  description="Try again a little later.",
                                  footer={"text":f"> Ref: `{ref}`"})

    @CogBase.listener()
    async def on_error(self, error):
        print("An error occurred:\n{}".format(error))
