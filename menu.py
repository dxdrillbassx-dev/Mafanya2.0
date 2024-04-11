import disnake
from disnake.ext import commands

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='menu', aliases=['help'])
    async def menu(self, ctx):
        """Отображает меню помощи."""
        embed = disnake.Embed(title="🤖 Меню помощи", description="Добро пожаловать! Я - ваш персональный бот.", color=0x7289DA)

        embed.set_footer(text=f"Запросил {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        # Получаем префикс команды
        prefix = self.bot.user.mention

        # Список команд с описаниями
        commands_list = [
            ("party", "Приглашает вас на вечеринку."),
            ("rules", "Отображает правила сервера."),
            # Добавьте сюда другие команды со списком и описанием
        ]

        for name, description in commands_list:
            embed.add_field(name=f"{prefix} {name}", value=description, inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Menu(bot))
