from discord.ext import commands
import asyncio
import discord
from botconstants import format_doc, EMOJI
from cogs.base import CogBase
import itertools as it


class RoleCog(CogBase):
    """Role and permission managing commands."""

    COLOUR = 0xFF00FF

    @commands.group(name="role", aliases=["roles"])
    async def role_group(self, _):
        """Role managing commands.

        Must have manage_roles permission to use."""
        pass

    @role_group.command(name="add")
    @commands.has_permissions(manage_roles=True)
    @format_doc
    async def role_add(self, ctx, rec: discord.Member, role: discord.Role):
        """Give a user an existing role.

        {}role add user role --> gives user the given role

        Must have role managing permissions."""
        await rec.add_roles(role)
        await self._send_simple(ctx, "Gave "+rec.mention+" the role "+role.name+".")

    @role_group.command(name="create")
    @commands.has_permissions(manage_roles=True)
    @format_doc
    async def role_create(self, ctx, role: str, copy_from: discord.Role = None):
        """Create a new role.

        {0}role create name --> makes a new role called "name"
        {0}role create name other_role --> makes a new role called "name" with the same perms as other_role

        Must have role managing permissions."""
        if copy_from is None:
            await ctx.guild.create_role(name=role)
        else:
            await ctx.guild.create_role(name=role, permissions=copy_from.permissions)
        await self._send_simple(ctx, "Created new role: " + role)

    @role_group.command(name="edit")
    @commands.has_permissions(manage_roles=True)
    @format_doc
    async def role_edit(self, ctx, role: discord.Role):
        """Edit existing role.

        {}role edit name --> opens Role Editor

        Role Editor
        Shows a list of 10 permissions on each page.
        Members with manage_roles permissions can react with the respective emoji to toggle the permission.
        React with ▶ to move to the next page.
        React with ❌ to close the editor."""
        reactants = EMOJI["DIGITS"] + [EMOJI["ARROWS"]["RIGHT"], EMOJI["CROSS_RED"]]
        async with ctx.typing():
            async def update_embed():
                ret = ""
                p_dict = dict(list(iter(role.permissions)))
                for i, r in enumerate(registers[reg_index]):
                    ret += reactants[i]+" "+r+" "+(EMOJI["TICK"] if p_dict[r] else EMOJI["CROSS_BLUE"])+"\n"
                return ret

            def c_check(c_reaction, c_user):
                return (c_user != msg.author and
                        c_user.permissions_in(msg.channel).manage_roles and
                        c_reaction.message.id == msg.id)

            def build_embed(desc):
                em = discord.Embed(title="Editing role: " + role.name, description=desc, colour=0x00ff00)
                em.set_footer(text="Role Editor")
                return em

            registers = []
            curr_reg = []

            for count, pair in zip(it.cycle(range(10)), role.permissions):
                curr_reg.append(pair[0])
                if count == 9:
                    registers.append(curr_reg[:])
                    curr_reg = []

            registers.append(curr_reg[:])
            reg_index = 0

            msg = await ctx.send(embed=build_embed(await update_embed()))

            for e in reactants:
                await msg.add_reaction(e)

        while True:
            e = build_embed(await update_embed())
            await msg.edit(embed=e)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=c_check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                msg.edit(embed=discord.Embed(title="Finished Editing Role: " + role.name,
                                             description="Timed out.",
                                             colour=0x00ff00))
                return
            if reaction.emoji == EMOJI["CROSS_RED"]:
                await msg.clear_reactions()
                await msg.edit(embed=discord.Embed(title="Finished Editing Role: "+role.name,
                                                   description="Closed manually.",
                                                   colour=0x00ff00))
                return
            if reaction.emoji == EMOJI["ARROWS"]["RIGHT"]:
                reg_index += 1
                if reg_index >= len(registers)-1:
                    reg_index = 0
                await reaction.remove(ctx.author)
            elif reaction.emoji in reactants:
                perm = registers[reg_index][reactants.index(reaction.emoji)]
                setattr(role.permissions, perm, not getattr(role.permissions, perm))
                await reaction.remove(user)
