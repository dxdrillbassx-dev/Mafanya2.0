import disnake
import pymysql
from disnake.ext import commands
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Отображение информации о пользователе")
    async def info(self, ctx, member: disnake.Member):
        if member is None:
            await ctx.send("Пользователь не найден.")
            return

        try:
            with self.bot.db.conn.cursor() as cursor:
                # Запросы для получения информации о пользователе
                sql_coins = "SELECT coins FROM user_coins WHERE user_id = %s"
                cursor.execute(sql_coins, (member.id,))
                result_coins = cursor.fetchone()
                coins = result_coins['coins'] if result_coins else 0

                sql_tokens = "SELECT tokens FROM user_tokens WHERE user_id = %s"
                cursor.execute(sql_tokens, (member.id,))
                result_tokens = cursor.fetchone()
                tokens = result_tokens['tokens'] if result_tokens else 0

                sql_messages = "SELECT COUNT(*) AS message_count FROM user_activity WHERE user_id = %s AND activity_type = 'Отправка сообщения'"
                cursor.execute(sql_messages, (member.id,))
                result_messages = cursor.fetchone()
                message_count = result_messages['message_count'] if result_messages else 0

                sql_last_activity = "SELECT MAX(activity_date) AS last_activity_date FROM user_activity WHERE user_id = %s"
                cursor.execute(sql_last_activity, (member.id,))
                result_last_activity = cursor.fetchone()
                last_activity_date = result_last_activity['last_activity_date'] if result_last_activity else None

                sql_mutes = "SELECT mute_count FROM user_mutes WHERE user_id = %s"
                cursor.execute(sql_mutes, (member.id,))
                result_mutes = cursor.fetchone()
                mute_count = result_mutes['mute_count'] if result_mutes else 0

                sql_warnings = "SELECT warn_count FROM user_warnings WHERE user_id = %s"
                cursor.execute(sql_warnings, (member.id,))
                result_warnings = cursor.fetchone()
                warn_count = result_warnings['warn_count'] if result_warnings else "Нету"

                roles = [role.name for role in member.roles if role.name != "@everyone"]
                roles_string = ", ".join(roles) if roles else "Нету"

                # Проверяем, есть ли у пользователя бан на сервере
                try:
                    ban_entry = await ctx.guild.fetch_ban(member)
                    has_ban = "✅ Забанен"
                except disnake.NotFound:
                    has_ban = "❌ Нет"

                # Получаем URL изображения пользователя
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

                # Создание embed с информацией о пользователе
                embed = disnake.Embed(
                    title=f"{member.name}",
                    description=f"Информация о пользователе",
                    color=disnake.Color.from_rgb(43, 45, 49)  # Изменение цвета на золотой
                )
                embed.set_thumbnail(url=avatar_url)  # Крупное изображение пользователя
                embed.add_field(name="🪙 Монеты", value=str(coins), inline=True)
                embed.add_field(name="🎟️ Жетоны", value=str(tokens), inline=True)
                embed.add_field(name="⠀", value="⠀", inline=False)  # Разделитель вместо "\u200b"
                embed.add_field(name="💬 Сообщения", value=str(message_count), inline=True)
                embed.add_field(name="⏱️ Последняя активность", value=last_activity_date, inline=True)
                embed.add_field(name="⠀", value="⠀", inline=False)  # Разделитель вместо "\u200b"
                embed.add_field(name="🔇 Муты", value=str(mute_count), inline=True)
                embed.add_field(name="⚠️ Предупреждения", value=str(warn_count), inline=True)
                embed.add_field(name="⠀", value="⠀", inline=False)  # Разделитель вместо "\u200b"
                embed.add_field(name="👥 Роли", value=roles_string, inline=False)
                embed.set_footer(text="Дополнительная информация о пользователе")  # Добавление подвала

                await ctx.send(embed=embed)

        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await ctx.send("Произошла ошибка при получении информации о пользователе.")

def setup(bot):
    bot.add_cog(Info(bot))
