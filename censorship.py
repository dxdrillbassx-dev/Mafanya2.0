from disnake.ext import commands

CENSORED_WORDS = ["блять", "сука"]  # Список цензуры
censorship_enabled = True  # Переменная для отслеживания включена ли фильтрация


class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global censorship_enabled
        if (
            censorship_enabled and not message.author.bot
        ):  # Проверяем, включена ли фильтрация и не является ли автор ботом
            for content in message.content.split():
                for censored_word in CENSORED_WORDS:
                    if content.lower() == censored_word:
                        await message.delete()
                        await message.channel.send(
                            f"{message.author.mention} такие слова запрещены!"
                        )

    @commands.slash_command(name="enable_censorship")
    @commands.has_permissions(administrator=True)
    async def _enable_censorship(self, ctx):
        global censorship_enabled
        censorship_enabled = True
        await ctx.respond(
            "Фильтрация включена!", ephemeral=True
        )  # Отправляем скрытое сообщение

    @commands.slash_command(name="disable_censorship")
    @commands.has_permissions(administrator=True)
    async def _disable_censorship(self, ctx):
        global censorship_enabled
        censorship_enabled = False
        await ctx.respond(
            "Фильтрация отключена!", ephemeral=True
        )  # Отправляем скрытое сообщение


def setup(bot):
    bot.add_cog(Censorship(bot))
