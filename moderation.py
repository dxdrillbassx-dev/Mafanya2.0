import asyncio

import disnake
from disnake.ext import commands
from db_connect import Database

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.slash_command(
        name="кик",
        description="Кикает пользователя с сервера"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter, member: disnake.Member, reason: str = "Нарушение правил!"):
        await inter.response.send_message(
            f"Администратор {inter.author.mention} исключил пользователя {member.mention} по причине: {reason}"
        )
        await member.kick(reason=reason)

    @commands.slash_command(
        name="бан",
        description="Банит пользователя на сервере"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter, member: disnake.Member, reason: str = "Нарушение правил!"):
        await inter.response.send_message(
            f"Администратор {inter.author.mention} забанил пользователя {member.mention} по причине: {reason}"
        )
        await member.ban(reason=reason)

    @commands.slash_command(
        name="очистка",
        description="Удаляет указанное количество сообщений"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter, amount: int):
        deleted = await inter.channel.purge(limit=amount + 1)
        await inter.response.send_message(f"Успешно удалено {len(deleted) - 1} сообщений!", ephemeral=True)

    @commands.slash_command()
    async def mute(self, interaction, member: disnake.Member, duration: int = None):
        mute_role = disnake.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role:
            await interaction.response.send_message(
                "Роль 'Muted' не найдена, создайте её для использования этой команды.")
            return

        # Добавляем информацию о муте в базу данных
        self.db.add_mute(member.id, duration)

        # Применяем мут на сервере
        await member.add_roles(mute_role)
        try:
            await interaction.response.defer()  # Откладываем отправку ответа
            await asyncio.sleep(1)  # Подождите немного, чтобы убедиться, что взаимодействие завершено
            await interaction.edit_original_message(content=f"{member.display_name} был заглушён на {duration} секунд.")

            if duration:
                await asyncio.sleep(duration)
                await member.remove_roles(mute_role)
                try:
                    await interaction.response.defer()  # Откладываем отправку ответа
                    await asyncio.sleep(1)  # Подождите немного, чтобы убедиться, что взаимодействие завершено
                    await interaction.edit_original_message(content=f"{member.display_name} теперь свободен от мута.")
                except Exception as e:
                    print(f"An error occurred while editing the message: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

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
