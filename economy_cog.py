import disnake
from disnake.ext import commands
import asyncio

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_balances = {}  # Словарь для хранения балансов пользователей

    @commands.slash_command()
    async def balance(self, interaction, member: disnake.Member = None):
        """ Показывает баланс пользователя. """
        user = member or interaction.author
        balance = self.user_balances.get(user.id, 0)
        await interaction.response.send_message(f"Баланс пользователя {user.display_name}: {balance} монет.")

    @commands.slash_command()
    async def add_coins(self, interaction, member: disnake.Member, amount: int):
        """ Добавляет монеты пользователю. Только для администраторов. """
        if not interaction.author.guild_permissions.administrator:
            await interaction.response.send_message("У вас нет прав администратора для выполнения этой команды.", ephemeral=True)
            return

        if member:
            self.user_balances[member.id] = self.user_balances.get(member.id, 0) + amount
            await interaction.response.send_message(f"Добавлено {amount} монет на счет пользователя {member.display_name}.")

    @commands.slash_command()
    async def transfer_coins(self, interaction, receiver: disnake.Member, amount: int):
        """ Передает монеты другому пользователю. """
        sender_id = interaction.author.id
        receiver_id = receiver.id

        if sender_id == receiver_id:
            await interaction.response.send_message("Вы не можете перевести монеты самому себе.", ephemeral=True)
            return

        if self.user_balances.get(sender_id, 0) < amount:
            await interaction.response.send_message("Недостаточно монет для выполнения перевода.", ephemeral=True)
            return

        self.user_balances[sender_id] -= amount
        self.user_balances[receiver_id] = self.user_balances.get(receiver_id, 0) + amount
        await interaction.response.send_message(f"Переведено {amount} монет пользователю {receiver.display_name}.")

    @commands.slash_command()
    async def buy_token(self, interaction, amount: int):
        """Покупает жетоны за монетки."""
        cost_per_token = 100  # Цена одного жетона в монетках (можете изменить по вашему усмотрению)
        total_cost = amount * cost_per_token

        if self.user_balances.get(interaction.author.id, 0) < total_cost:
            await interaction.response.send_message("У вас недостаточно монет для покупки жетонов.", ephemeral=True)
            return

        self.user_balances[interaction.author.id] -= total_cost
        tokens_owned = self.user_balances.get(f"{interaction.author.id}_tokens", 0)
        self.user_balances[f"{interaction.author.id}_tokens"] = tokens_owned + amount
        await interaction.response.send_message(f"Вы купили {amount} жетонов за {total_cost} монет.")

    @commands.slash_command()
    async def change_nickname(self, interaction, new_nickname: str):
        """Меняет никнейм пользователя за жетон."""
        cost_per_nickname_change = 1  # Цена одной смены никнейма в жетонах (можете изменить по вашему усмотрению)

        if self.user_balances.get(f"{interaction.author.id}_tokens", 0) < cost_per_nickname_change:
            await interaction.response.send_message("У вас недостаточно жетонов для смены никнейма.", ephemeral=True)
            return

        # Вычитаем стоимость смены никнейма из баланса жетонов
        self.user_balances[f"{interaction.author.id}_tokens"] -= cost_per_nickname_change

        # Здесь можно добавить код для смены никнейма пользователя, используя disnake

        await interaction.response.send_message(f"Никнейм изменен на {new_nickname}.")

def setup(bot):
    bot.add_cog(Economy(bot))
