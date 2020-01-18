from discord.ext import commands
import asyncio
import discord
import re
from utils import format_doc
from cogs.base import CogBase
import itertools as it
from utils.botconstants import EMOJI


class RoleCog(CogBase, name="Roles and Permissions"):
    """Role and permission managing commands."""

    COLOUR = 0xFF00FF

    @commands.group(name="role", aliases=["roles"])
    async def role_group(self, _):
        """Role managing commands.

        Must have manage_roles permission to use."""

    @role_group.command(name="add")
    @commands.has_permissions(manage_roles=True)
    @format_doc
    async def role_add(self, ctx, recipient: discord.Member, role: discord.Role):
        """Give a user an existing role.

        {}role add user role --> gives user the given role

        Must have role managing permissions."""
        await recipient.add_roles(role)
        await self._send_simple(ctx, "Gave " + recipient.mention + " the role " + role.name + ".")

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
        check = f"\N{BALLOT BOX WITH CHECK}\N{VARIATION SELECTOR-16}"
        reactants = EMOJI["DIGITS"] + [f"\N{BLACK RIGHT-POINTING TRIANGLE}", f"\N{CROSS MARK}"]
        async with ctx.typing():
            async def update_embed():
                ret = ""
                p_dict = dict(list(iter(role.permissions)))
                for i, r in enumerate(registers[reg_index]):
                    ret += reactants[i]+" {} {}\n".format(re.sub("_", " ", r),
                                                          (f"\N{NEGATIVE SQUARED CROSS MARK}" if p_dict[r] else check))
                return ret

            def c_check(c_reaction, c_user):
                return (c_user != msg.author and
                        c_user.permissions_in(msg.channel).manage_roles and
                        c_reaction.message.id == msg.id)

            def build_embed(desc):
                em = self.build_embed(title="Editing role: " + role.name,
                                      description=desc, colour=role.colour,
                                      footer={"text": f"Role Editor | Page {reg_index+1} of {len(registers)-1}"})
                return em

            registers = []
            curr_reg = []

            for count, (perm, _) in zip(it.cycle(range(10)), role.permissions):
                curr_reg.append(perm)
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
                await msg.edit(embed=self.build_embed(title="Finished Editing Role: "+role.name,
                                                      description="Timed out."))
                return
            if reaction.emoji == f"\N{CROSS MARK}":
                await msg.clear_reactions()
                await msg.edit(embed=self.build_embed(title="Finished Editing Role: "+role.name,
                                                      description="Closed manually."))
                return
            if reaction.emoji == f"\N{BLACK RIGHT-POINTING TRIANGLE}":
                reg_index += 1
                if reg_index >= len(registers)-1:
                    reg_index = 0
                await reaction.remove(ctx.author)
            elif reaction.emoji in reactants:
                perm = registers[reg_index][reactants.index(reaction.emoji)]
                setattr(role.permissions, perm, not getattr(role.permissions, perm))
                await reaction.remove(user)
