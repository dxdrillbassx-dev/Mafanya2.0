import disnake
from disnake.ext import commands


class Top(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.slash_command(
        description="Показывает топ пользователей по активности на сервере"
    )
    async def top(self, inter: disnake.ApplicationCommandInteraction):
        try:
            # Получаем топ пользователей по количеству активности
            top_users = self.db.get_top_users(20)
            if not top_users:
                await inter.response.send_message(
                    embed=self.create_empty_embed()
                )
                return

            # Формируем embed с топом пользователей
            embed = self.create_top_embed(inter.guild, top_users)

            # Отправляем embed с топом пользователей
            await inter.response.send_message(embed=embed)
        except Exception as e:
            await self.handle_error(inter, e)

    async def handle_error(self, inter: disnake.ApplicationCommandInteraction, error: Exception):
        embed = disnake.Embed(
            title="Ошибка", description=f"Произошла ошибка: {error}", color=disnake.Color.red()
        )
        await inter.response.send_message(embed=embed)
        print(f"Ошибка в команде top: {error}")

    def create_empty_embed(self):
        embed = disnake.Embed(
            title="Топ пользователей по активности",
            description="Нет данных о активности пользователей.",
            color=disnake.Color.red()
        )
        embed.set_thumbnail(url=self.bot.guild.icon.url)
        embed.set_footer(text=f"Участников на сервере: {self.bot.guild.member_count}")
        return embed

    def create_top_embed(self, guild, top_users):
        embed = disnake.Embed(
            title="Топ пользователей по активности", color=disnake.Color.green()
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"Участников на сервере: {guild.member_count}")
        for idx, user in enumerate(top_users, 1):
            member = guild.get_member(user["user_id"])
            name = member.display_name if member else f"Пользователь с ID {user['user_id']}"
            icon_url = member.avatar.url if member else disnake.Embed.Empty
            embed.add_field(
                name=f"{idx}. {name}",
                value=f"Активность: {user['activity_count']} активностей",
                inline=False
            )
            embed.set_thumbnail(url=icon_url)  # Перемещена эта строка
        return embed


def setup(bot):
    from db_connect import Database
    db = Database()
    try:
        db.connect()
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    bot.add_cog(Top(bot, db))
