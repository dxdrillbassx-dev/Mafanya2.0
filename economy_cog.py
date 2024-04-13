import disnake
from disnake.ext import commands
import pymysql

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def balance(self, interaction, member: disnake.Member = None):
        """ Показывает баланс пользователя. """
        user = member or interaction.author
        try:
            with self.bot.db.conn.cursor() as cursor:
                sql = "SELECT coins FROM user_coins WHERE user_id = %s"
                cursor.execute(sql, (user.id,))
                result = cursor.fetchone()
                balance = result['coins'] if result else 0
                await interaction.response.send_message(f"Баланс пользователя {user.display_name}: {balance} монет.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await interaction.response.send_message("Произошла ошибка при попытке получить баланс пользователя.", ephemeral=True)

    @commands.slash_command()
    async def add_coins(self, interaction, member: disnake.Member, amount: int):
        """ Добавляет монеты пользователю. Только для администраторов. """
        if not interaction.author.guild_permissions.administrator:
            await interaction.response.send_message("У вас нет прав администратора для выполнения этой команды.", ephemeral=True)
            return

        try:
            with self.bot.db.conn.cursor() as cursor:
                sql = "INSERT INTO user_coins (user_id, coins) VALUES (%s, %s) ON DUPLICATE KEY UPDATE coins = coins + %s"
                cursor.execute(sql, (member.id, amount, amount))
                self.bot.db.conn.commit()
                await interaction.response.send_message(f"Добавлено {amount} монет на счет пользователя {member.display_name}.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await interaction.response.send_message("Произошла ошибка при попытке добавить монеты пользователю.", ephemeral=True)

    @commands.slash_command()
    async def transfer_coins(self, interaction, receiver: disnake.Member, amount: int):
        """ Передает монеты другому пользователю. """
        sender_id = interaction.author.id
        receiver_id = receiver.id

        if sender_id == receiver_id:
            await interaction.response.send_message("Вы не можете перевести монеты самому себе.", ephemeral=True)
            return

        try:
            with self.bot.db.conn.cursor() as cursor:
                sql = "SELECT coins FROM user_coins WHERE user_id = %s"
                cursor.execute(sql, (sender_id,))
                sender_balance = cursor.fetchone()['coins']

                if sender_balance < amount:
                    await interaction.response.send_message("Недостаточно монет для выполнения перевода.", ephemeral=True)
                    return

                # Обновляем балансы отправителя и получателя в базе данных
                sql = "UPDATE user_coins SET coins = coins - %s WHERE user_id = %s"
                cursor.execute(sql, (amount, sender_id))
                sql = "INSERT INTO user_coins (user_id, coins) VALUES (%s, %s) ON DUPLICATE KEY UPDATE coins = coins + %s"
                cursor.execute(sql, (receiver_id, amount, amount))
                self.bot.db.conn.commit()
                await interaction.response.send_message(f"Переведено {amount} монет пользователю {receiver.display_name}.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await interaction.response.send_message("Произошла ошибка при попытке перевести монеты.", ephemeral=True)

    @commands.slash_command()
    async def buy_token(self, interaction, amount: int):
        """Покупает жетоны за монетки."""
        cost_per_token = 100  # Цена одного жетона в монетках (можете изменить по вашему усмотрению)
        total_cost = amount * cost_per_token

        try:
            with self.bot.db.conn.cursor() as cursor:
                # Проверяем, достаточно ли у пользователя монет для покупки жетонов
                sql = "SELECT coins FROM user_coins WHERE user_id = %s"
                cursor.execute(sql, (interaction.author.id,))
                user_balance = cursor.fetchone()['coins']
                if user_balance < total_cost:
                    await interaction.response.send_message("У вас недостаточно монет для покупки жетонов.",
                                                            ephemeral=True)
                    return

                # Вычитаем стоимость жетонов из баланса пользователя
                sql = "UPDATE user_coins SET coins = coins - %s WHERE user_id = %s"
                cursor.execute(sql, (total_cost, interaction.author.id))

                # Добавляем жетоны пользователю в таблицу tokens
                sql = "INSERT INTO user_tokens (user_id, tokens) VALUES (%s, %s) ON DUPLICATE KEY UPDATE tokens = tokens + %s"
                cursor.execute(sql, (interaction.author.id, amount, amount))
                self.bot.db.conn.commit()

                await interaction.response.send_message(f"Вы купили {amount} жетонов за {total_cost} монет.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await interaction.response.send_message("Произошла ошибка при попытке купить жетоны.", ephemeral=True)

    @commands.slash_command()
    async def change_nickname(self, interaction, new_nickname: str):
        """Меняет никнейм пользователя за жетон."""
        cost_per_nickname_change = 1  # Цена одной смены никнейма в жетонах (можете изменить по вашему усмотрению)

        try:
            with self.bot.db.conn.cursor() as cursor:
                sql = "SELECT coins FROM user_coins WHERE user_id = %s"
                cursor.execute(sql, (interaction.author.id,))
                user_tokens = cursor.fetchone()['coins']

                if user_tokens < cost_per_nickname_change:
                    await interaction.response.send_message("У вас недостаточно жетонов для смены никнейма.", ephemeral=True)
                    return

                # Вычитаем стоимость смены никнейма из баланса жетонов
                sql = "UPDATE user_coins SET coins = coins - %s WHERE user_id = %s"
                cursor.execute(sql, (cost_per_nickname_change, interaction.author.id))
                self.bot.db.conn.commit()

                # Здесь можно добавить код для смены никнейма пользователя, используя disnake

                await interaction.response.send_message(f"Никнейм изменен на {new_nickname}.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при выполнении запроса к базе данных:")
            print(e)
            await interaction.response.send_message("Произошла ошибка при попытке смены никнейма.", ephemeral=True)

def setup(bot):
    bot.add_cog(Economy(bot))
