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
        selected_value = self.values[0]  # Получаем выбранное значение как строку

        embed = disnake.Embed(
            title=f"Правила сервера: {selected_value}",
            color=0x2F3136
        )

        if selected_value == "Контент 18+":
            embed.add_field(name="Правило 1", value="Текст правила 1", inline=True)
            embed.add_field(name="Правило 2", value="Текст правила 2", inline=True)
            embed.add_field(name="Правило 3", value="Текст правила 3", inline=True)
            embed.add_field(name="Правило 4", value="Текст правила 4", inline=True)
        elif selected_value == "Чистота чатов и неприятные темы":
            embed.add_field(name="Правило 1", value="Текст правила 1", inline=True)
            embed.add_field(name="Правило 2", value="Текст правила 2", inline=True)
            embed.add_field(name="Правило 3", value="Текст правила 3", inline=True)
            embed.add_field(name="Правило 4", value="Текст правила 4", inline=True)

        # Проверяем, был ли ответ на взаимодействие уже отправлен
        if interaction.response.is_done():
            # Если ответ уже был отправлен, редактируем сообщение
            await interaction.edit_original_message(embed=embed, view=DropdownView())
        else:
            # Если ответ еще не был отправлен, отправляем новое сообщение с embed и view
            await interaction.response.send_message(embed=embed, view=DropdownView(), ephemeral=True)


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMenu())

def setup(bot):
    bot.add_cog(RulesMenu(bot))
