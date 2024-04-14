import disnake
from disnake.ext import commands


class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="party", description="Приглашает пользователя на вечеринку."
    )
    async def party(self, inter: disnake.ApplicationCommandInteraction):
        """Приглашает пользователя на вечеринку."""
        view = Confirm()
        await inter.response.send_message(
            "Приглашение на вечеринку, согласен ли ты принять его?", view=view
        )
        await view.wait()

        if view.value is None:
            await inter.response.send_message("Ты упустил свой шанс!")
        elif view.value:
            await inter.response.send_message(
                "Отлично, держи ссылку!", view=LinkToParty()
            )
        else:
            await inter.response.send_message("Ну и ладно 😕")


class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10.0)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, emoji="😎")
    async def confirm(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.edit_message(
            content="Отлично, жди ссылку на вступление!", view=None
        )
        # Отправляем новое сообщение с дополнительной кнопкой
        view = LinkToParty()
        await inter.followup.send("Держи ссылку на вечеринку!", view=view)

    @disnake.ui.button(label="Отмена", style=disnake.ButtonStyle.red, emoji="🥱")
    async def cancel(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.edit_message(content="Хорошо, я тебя поняла.", view=None)
        self.stop()


class LinkToParty(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Жмякни",
                url="https://www.youtube.com/watch?v=9j4HJp-AsOo",
                style=disnake.ButtonStyle.green,
                emoji="😘",
            )
        )


def setup(bot):
    bot.add_cog(Party(bot))