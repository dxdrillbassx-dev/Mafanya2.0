import disnake
from disnake.ext import commands
from disnake.ui import Button, View

class ProfileView(View):
    def __init__(self):
        super().__init__()

        # Добавляем кнопки в вид, разбивая их по три в каждой строке
        buttons = [
            [
                Button(label="💰 Монетки", custom_id="coins", style=disnake.ButtonStyle.grey),
                Button(label="🏷️ Никнейм", custom_id="nickname", style=disnake.ButtonStyle.grey),
                Button(label="🎭 Роли", custom_id="roles", style=disnake.ButtonStyle.grey)
            ],
            [
                Button(label="🎒 Инвентарь", custom_id="inventory", style=disnake.ButtonStyle.grey),
                Button(label="👗 Гардероб", custom_id="wardrobe", style=disnake.ButtonStyle.grey),
                Button(label="🎂 День рождения", custom_id="birthday", style=disnake.ButtonStyle.grey)
            ],
            [
                Button(label="📊 Статистика", custom_id="statistics", style=disnake.ButtonStyle.grey),
                Button(label="🔖 Промокод", custom_id="promo_code", style=disnake.ButtonStyle.grey),
                Button(label="🏆 Достижения", custom_id="achievements", style=disnake.ButtonStyle.grey)
            ]
        ]

        for row in buttons:
            for button in row:
                self.add_item(button)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def profile(self, interaction: disnake.ApplicationCommandInteraction):
        """Показывает профиль пользователя с интерактивными кнопками."""
        # Создаем вид с кнопками
        view = ProfileView()
        # Отправляем сообщение с прикрепленным видом
        await interaction.response.send_message("Профиль пользователя:", view=view)

def setup(bot):
    bot.add_cog(Profile(bot))
