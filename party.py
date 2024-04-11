import disnake
from disnake.ext import commands

class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def party(self, ctx):
        """Приглашает пользователя на вечеринку."""
        view = Confirm()
        await ctx.send("Приглашение на вечеринку, согласен ли ты принять его?", view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Ты упустил свой шанс!")
        elif view.value:
            await ctx.send("Отлично, держи ссылку!", view=LinkToParty())
        else:
            await ctx.send("Ну и хуй тебе")

class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10.0)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, emoji="😎")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(content="Отлично, жди ссылку на вступление!", view=None)
        # Отправляем новое сообщение с дополнительной кнопкой
        view = LinkToParty()
        await inter.followup.send("Держи ссылку на вечеринку!", view=view)

    @disnake.ui.button(label="Отмена", style=disnake.ButtonStyle.red, emoji="🥱")
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(content="Хорошо, я тебя поняла.", view=None)
        self.stop()

class LinkToParty(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(label="Жмякни", url="https://www.youtube.com/watch?v=9j4HJp-AsOo", style=disnake.ButtonStyle.green, emoji="😘"))

def setup(bot):
    bot.add_cog(Party(bot))
