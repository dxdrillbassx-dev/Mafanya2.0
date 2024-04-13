import disnake
from disnake.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="кик", aliases=["кыш", "выгнать"], usage="kick <@user> <reason=None>", brief="Кикает пользователя с сервера")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason="Нарушение правил!"):
        await ctx.send(f"Администратор {ctx.author.mention} исключил пользователя {member.mention} по причине: {reason}")
        await member.kick(reason=reason)

    @commands.slash_command()
    async def kick(self, interaction, member: disnake.Member, reason: str = "Нарушение правил!"):
        await interaction.response.send_message(
            f"Администратор {interaction.author.mention} исключил пользователя {member.mention} по причине: {reason}")
        await member.kick(reason=reason)

    @commands.command(name="бан", aliases=["баня", "банан"], usage="ban <@user> <reason=None>", brief="Банит пользователя на сервере")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member, *, reason="Нарушение правил!"):
        await ctx.send(f"Администратор {ctx.author.mention} забанил пользователя {member.mention} по причине: {reason}")
        await member.ban(reason=reason)

    @commands.command(name="очистка", aliases=["очистить", "clear"], usage="clear <количество сообщений>", brief="Удаляет указанное количество сообщений")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Успешно удалено {len(deleted)-1} сообщений!", delete_after=5)

    @commands.command(name="мут", aliases=["mute"], usage="mute <@участник> <время в секундах>", brief="Мутит пользователя на сервере")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: disnake.Member, duration: int = None):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Роль 'Muted' не найдена, создайте её для использования этой команды.")
            return
        await member.add_roles(mute_role)
        await ctx.send(f"{member.display_name} был заглушён на {duration} секунд.")
        if duration:
            await asyncio.sleep(duration)
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.display_name} теперь свободен от мута.")

    @commands.command(name="размут", aliases=["unmute"], usage="unmute <@участник>", brief="Снимает мут с пользователя")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"Мут с пользователя {member.display_name} снят.")
        else:
            await ctx.send("У пользователя нет мута.")

    @commands.command(name="разбан", aliases=["unban"], usage="unban <ID пользователя>", brief="Снимает бан с пользователя")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_id: int):
        user = await self.bot.fetch_user(member_id)
        await ctx.guild.unban(user)
        await ctx.send(f"Пользователь {user.display_name} разбанен.")

    @commands.command(name="ник", aliases=["nick", "nickname"], usage="nick <@участник> <новый ник>", brief="Изменяет никнейм пользователя")
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: disnake.Member, *, new_nick: str):
        await member.edit(nick=new_nick)
        await ctx.send(f"Никнейм пользователя {member.display_name} изменён на {new_nick}.")

    @commands.command(name="перенос", aliases=["move"], usage="move <@участник> <ID канала>", brief="Перемещает пользователя в другой голосовой канал")
    @commands.has_permissions(move_members=True)
    async def move(self, ctx, member: disnake.Member, channel: disnake.VoiceChannel):
        await member.move_to(channel)
        await ctx.send(f"Пользователь {member.display_name} перемещён в канал {channel.name}.")

    @commands.command(name="предупреждение", aliases=["warn"], usage="warn <@участник> <причина>", brief="Выдаёт предупреждение пользователю")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: disnake.Member, *, reason: str):
        # Здесь должна быть реализация логики предупреждений (например, запись в базу данных)
        await ctx.send(f"Пользователю {member.display_name} выдано предупреждение по причине: {reason}")

    @commands.command(name="активность", aliases=["activity"], usage="activity <@участник>", brief="Показывает активность пользователя на сервере")
    async def activity(self, ctx, member: disnake.Member):
        # Здесь должна быть реализация просмотра активности (например, запрос к базе данных)
        await ctx.send(f"Активность пользователя {member.display_name} на сервере.")

    @commands.slash_command()
    async def avatar(self, interaction, member: disnake.Member = None):
        user = member or interaction.author  # Обеспечиваем возможность выбора пользователя, или использование автора команды по умолчанию
        embed = disnake.Embed(title=f"Avatar of {user.display_name}",
                              color=0x2f3136)  # Название эмбеда с именем пользователя
        embed.set_image(url=user.display_avatar.url)  # Установка изображения аватара пользователя
        await interaction.response.send_message(embed=embed)  # Отправка эмбеда

def setup(bot):
    bot.add_cog(Moderation(bot))
