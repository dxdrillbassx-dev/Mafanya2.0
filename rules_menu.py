import disnake
from disnake.ext import commands

class RulesMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):
        """Отправляет сообщение с выпадающим списком правил."""
        await ctx.send("Выберите правило для детального просмотра:", view=DropdownView())

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
            placeholder="Вам также может быть интересно",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: disnake.Interaction):
        rules_text = {
            "Контент 18+": "Текст правила для контента 18+...",
            "Чистота чатов и неприятные темы": "Текст правила про чистоту чатов...",
            "Вежливость": "Текст правила про вежливость...",
            "Реклама и услуги": "Текст правила про рекламу и услуги...",
            "Серверный профиль": "Текст правила про серверный профиль...",
            "Злоупотребление системой": "Текст правила про злоупотребление системой...",
            "Право модератора": "Текст правила про права модератора...",
        }

        selected_rule = self.values[0]
        rule_text = rules_text.get(selected_rule, "Правило не найдено.")

        await interaction.response.edit_message(content=f"**Выбранное правило:**\n{rule_text}", view=self.view)

class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMenu())

def setup(bot):
    bot.add_cog(RulesMenu(bot))
