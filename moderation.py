import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="кик", aliases=["кыш", "выгнать"], usage="kick <@user> <reason=None>")
    @commands.has_permissions(kick_members=True, administrator=True)
    async def kick(self, ctx, member: disnake.Member, *, reason="Нарушение правил!"):
        await ctx.send(f"Администратор {ctx.author.mention} исключил пользователя {member.mention}")
        await member.kick(reason=reason)
        await ctx.message.delete()

    @commands.command(name="бан", aliases=["баня", "банан"], usage="ban <@user> <reason=None>")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban(self, ctx, member: disnake.Member, *, reason="Нарушение правил!"):
        await ctx.send(f"Администратор {ctx.author.mention} забанил пользователя {member.mention}")
        await member.ban(reason=reason)
        await ctx.message.delete()

