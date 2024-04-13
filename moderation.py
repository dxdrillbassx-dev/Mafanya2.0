import asyncio
from datetime import datetime
import disnake
import pymysql
from disnake.ext import commands
from db_connect import Database

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

#kick - КИК
    @commands.slash_command(
        description="Кикает пользователя с сервера."
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter, member: disnake.Member, reason: str = "Нарушение правил!"):
        await inter.response.send_message(
            f"Администратор {inter.author.mention} исключил пользователя {member.mention} по причине: {reason}"
        )
        await member.kick(reason=reason)

#/ban - БАН
    @commands.slash_command(
        description="Банит пользователя на сервере."
    )
    async def ban(self, interaction, member: disnake.Member, *, reason: str = "Нарушение правил!"):
        try:
            await interaction.response.defer()

            await member.ban(reason=reason)

            await interaction.edit_original_message(
                content=f"Администратор {interaction.author.mention} забанил пользователя {member.mention} по причине: {reason}")
        except disnake.NotFound:
            print("Interaction not found. Ignoring the command.")
        except Exception as e:
            print(f"An error occurred: {e}")

#/clear - ОЧИСТКА ЧАТА
    @commands.slash_command(
        description="Удаляет указанное количество сообщений."
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter, amount: int):
        deleted = await inter.channel.purge(limit=amount + 1)
        await inter.response.send_message(f"Успешно удалено {len(deleted) - 1} сообщений!", ephemeral=True)

#/mute - МУТ
    @commands.slash_command(
        description="Мутит человека на сервере."
    )
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
                    print(f"- [Mafanya] Ошибка: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

#/unmute - РАЗМУТ
    @commands.command(name="размут", aliases=["unmute"], usage="unmute <@участник>", brief="Снимает мут с пользователя")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"Мут с пользователя {member.display_name} снят.")
        else:
            await ctx.send("У пользователя нет мута.")

#/unban - РАЗБАН
    @commands.slash_command(
        description="Разбанивает человека на сервере."
    )
    async def unban(self, interaction, *, member_id: int):
        try:
            user = await self.bot.fetch_user(member_id)
            await interaction.guild.unban(user)
            await interaction.response.send_message(content=f"Пользователь {user.display_name} разбанен.")
        except disnake.NotFound:
            await interaction.response.send_message(content="Пользователь с таким ID не найден.")
        except Exception as e:
            await interaction.response.send_message(content=f"Произошла ошибка: {e}")

#/nickname - СМЕНА НИКНЕЙМА
    @commands.slash_command(
        name="nick",
        description="Изменяет никнейм пользователя",
        guild_ids=[1227760104963837952]
    )
    async def nickname(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, new_nick: str):
        if inter.author.guild_permissions.manage_nicknames:
            await member.edit(nick=new_nick)
            await inter.response.send_message(f"Никнейм пользователя {member.display_name} изменён на {new_nick}.")
        else:
            await inter.response.send_message("У вас недостаточно прав для выполнения этой команды.")

#/warn - ПРЕДУПРЕЖДЕНИЯ
    @commands.slash_command(
        description="Выдаёт предупреждение пользователю"
    )
    @commands.has_permissions(kick_members=True)
    async def warn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, *, reason: str):
        # Добавляем предупреждение в базу данных
        self.db.add_warning(member.id)

        # Проверяем количество предупреждений пользователя
        self.db.check_warnings(member.id)

        # Отправляем сообщение о выдаче предупреждения
        await inter.response.send_message(
            f"Пользователю {member.display_name} выдано предупреждение по причине: {reason}")

#/activity - АКТИВНОСТЬ(ЛОГИ)
    async def log_activity(self, user_id, activity_type):
        try:
            with self.db.conn.cursor() as cursor:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO user_activity (user_id, activity_date, activity_type) VALUES (%s, %s, %s)",
                               (user_id, current_time, activity_type))
            self.db.conn.commit()
            print("- [Mafanya] Запись активности успешно добавлена в базу данных.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при добавлении записи активности в базу данных:")
            print(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.log_activity(message.author.id, "Отправка сообщения")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return
        if after.channel:
            await self.log_activity(member.id, "Подключение к голосовому каналу")

# /activity - АКТИВНОСТЬ
    @commands.slash_command(
        description="Показывает активность пользователя на сервере"
    )
    async def activity(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user_activity WHERE user_id = %s", (member.id,))
                activities = cursor.fetchall()
                if activities:
                    activity_list = "\n".join(
                        f"{activity['activity_date']}: {activity['activity_type']}" for activity in activities)
                    message = f"Активность пользователя {member.display_name} на сервере:\n{activity_list}"
                else:
                    message = f"Пользователь {member.display_name} еще не проявлял активности на сервере."
                await inter.response.send_message(message)
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при запросе активности пользователя из базы данных:")
            print(e)


#/avatar - АВАТАР
    @commands.slash_command(
        description="Показывает аватар человека на сервере."
    )
    async def avatar(self, interaction, member: disnake.Member = None):
        user = member or interaction.author  # Обеспечиваем возможность выбора пользователя, или использование автора команды по умолчанию
        embed = disnake.Embed(title=f"Avatar of {user.display_name}",
                              color=0x2f3136)  # Название эмбеда с именем пользователя
        embed.set_image(url=user.display_avatar.url)  # Установка изображения аватара пользователя
        await interaction.response.send_message(embed=embed)  # Отправка эмбеда

def setup(bot):
    bot.add_cog(Moderation(bot))
