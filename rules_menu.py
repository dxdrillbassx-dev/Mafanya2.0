import disnake
from disnake.ext import commands
from disnake import Embed

class RulesMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):
        """Отправляет сообщение с кнопкой, при нажатии на которую появляется DropdownMenu."""
        # Создаём кнопку
        button = disnake.ui.Button(emoji="🛡", label="Узнать подробности системы и правил", style=disnake.ButtonStyle.gray)
        # Создаем view и добавляем в него кнопку
        view = disnake.ui.View()
        view.add_item(button)
        # Ожидаем нажатия на кнопку
        async def button_callback(interaction):
            # Создаем DropdownView и добавляем в него DropdownMenu
            dropdown_view = DropdownView()
            await interaction.response.send_message("Выберите пункт правил:", view=dropdown_view, ephemeral=True)
        # Привязываем callback функцию к кнопке
        button.callback = button_callback
        # Отправляем сообщение с кнопкой
        await ctx.send("Нажмите на кнопку, чтобы узнать правила:", view=view)

class DropdownMenu(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Контент 18+", description="Недетский контент, общение на тему NSFW", emoji="🔞"),
            disnake.SelectOption(label="Чистота чатов и неприятные темы", description="Спам, флуд и политика", emoji="🗑"),
            disnake.SelectOption(label="Вежливость", description="Уважение к другим, токсичность", emoji="❤"),
            disnake.SelectOption(label="Реклама и услуги", description="Назойливая реклама услуг и продуктов", emoji="🔔"),
            disnake.SelectOption(label="Серверный профиль", description="Неподобающие ники, клоны чужих профилей", emoji="🌈"),
            disnake.SelectOption(label="Злоупотребление системой", description="Репорты без причины, твинки", emoji="💂‍♂️"),
            disnake.SelectOption(label="Право модератора", description="Наказания на усмотрение модерации", emoji="⚠"),
        ]

        super().__init__(
            placeholder="Выберите пункт правил...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: disnake.Interaction):
        # Создание объекта Embed с общим заголовком и цветом
        embed = Embed(
            title="Правила сервера",
            color=0x2F3136  # Цвет фона Discord для лучшей интеграции
        )

        # Добавление полей в embed.
        # Параметр inline=True означает, что поля будут расположены в одну линию, если есть достаточно места
        embed.add_field(name="🔞 КОНТЕНТ 18+", value="Текст правила для контента 18+...", inline=True)
        embed.add_field(name="📛 НЕПРИЯТНОЕ ОБЩЕНИЕ",
                        value="Если вы видите что-то, что нарушает правила или неуместно, пожалуйста, сообщите об этом в канал #поддержка команды /report",
                        inline=True)

        # Так как Discord не поддерживает диагональное размещение, мы используем следующую строчку для симуляции этого.
        embed.add_field(name="\u200B", value="\u200B",
                        inline=False)  # Добавляем пустое поле, чтобы создать разрыв между строками

        embed.add_field(name="🧹 ЧИСТОТА ЧАТОВ И НЕПРИЯТНЫЕ ТЕМЫ", value="Текст правила про чистоту чатов...",
                        inline=True)
        embed.add_field(name="🤝 ВЕЖЛИВОСТЬ", value="Текст правила про вежливость...", inline=True)

        # Передаем embed как ответ на взаимодействие
        await interaction.response.edit_message(content=None, embed=embed, view=self.view)

class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMenu())

def setup(bot):
    bot.add_cog(RulesMenu(bot))
