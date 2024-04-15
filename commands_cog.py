import disnake
from disnake.ext import commands

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="commands",
        description="Показывает список команд",
    )
    async def commands(self, inter: disnake.ApplicationCommandInteraction):
        # Создаем кнопки для различных категорий команд
        button_general = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Общие", emoji="ℹ️")
        button_fun = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Развлечения", emoji="🎉")
        button_economy = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Экономика", emoji="💰")
        button_admin = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Админ", emoji="🛠️")

        # Создаем встраиваемое сообщение с кнопками и текстом
        embed = disnake.Embed(title="Выберите категорию команд:", color=0x7289DA)
        await inter.response.send_message(
            embed=embed,
            components=[[button_general, button_fun], [button_economy, button_admin]]
        )

        # Функция для обработки нажатий на кнопки
        async def button_callback(interaction):
            if interaction.component.label == "Общие":
                embed = disnake.Embed(title="Общие команды", description="Список общих команд:")
                embed.add_field(name="/commands", value="Показывает список команд")
                embed.add_field(name="/profile", value="Показывает профиль пользователя")
                embed.add_field(name="/rules", value="Узнать подробности системы и правил")
                embed.add_field(name="/info", value="Отображение информации о пользователе")
                embed.add_field(name="/top", value="Показывает топ пользователей")
                embed.add_field(name="+", value="Ответ на сообщение ставит реакцию")
            elif interaction.component.label == "Развлечения":
                embed = disnake.Embed(title="Команды развлечений", description="Список команд развлечений:")
                embed.add_field(name="/calc", value="Простой калькулятор")
                embed.add_field(name="/party", value="Приглашает пользователя на вечеринку")
            elif interaction.component.label == "Экономика":
                embed = disnake.Embed(title="Команды экономики", description="Список команд экономики:")
                embed.add_field(name="/balance", value="Показывает баланс пользователя")
                embed.add_field(name="/transfer_coins", value="Передает монеты другому пользователю")
                embed.add_field(name="/buy_token", value="Покупает жетоны за монетки")
                embed.add_field(name="/change_nickname", value="Меняет никнейм пользователя за жетон")
            elif interaction.component.label == "Админ":
                embed = disnake.Embed(title="Административные команды", description="Список административных команд:")
                embed.add_field(name="/enable_censorship", value="Фильтрация включена")
                embed.add_field(name="/disable_censorship", value="Фильтрация отключена")
                embed.add_field(name="/add_coins", value="Добавляет монеты пользователю")
                embed.add_field(name="/kick", value="Кикает пользователя с сервера")
                embed.add_field(name="/ban", value="Банит пользователя на сервере")
                embed.add_field(name="/clear", value="Удаляет указанное количество сообщений")
                embed.add_field(name="/mute", value="Мутит человека на сервере")
                embed.add_field(name="/unmute", value="Снимает мут с пользователя")
                embed.add_field(name="/nick", value="Изменяет никнейм пользователя")
                embed.add_field(name="/warn", value="Выдаёт предупреждение пользователю")
                embed.add_field(name="/activity", value="Показывает активность пользователя на сервере")
                embed.add_field(name="/avatar", value="Показывает аватар человека на сервере")
                embed.add_field(name="/enable_caps_filter", value="Включить фильтр капса")
                embed.add_field(name="/disable_caps_filter", value="Выключить фильтр капса")
            else:
                embed = disnake.Embed(title="Ошибка", description="Непредвиденное действие")

            await inter.edit_original_message(embed=embed)

        # Добавляем обработчик для кнопок
        self.bot.add_listener(button_callback, "on_button_click")

def setup(bot):
    bot.add_cog(CommandsCog(bot))
