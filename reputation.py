import disnake
from disnake.ext import commands
from disnake.ext.commands import CheckFailure


class Reputation(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.bot.user:
            return

        # Проверяем, есть ли "+" в начале сообщения и упоминание пользователей
        if message.content.startswith('+') and message.mentions:
            # Добавляем репутацию первому упомянутому пользователю
            user_to_rep = message.mentions[0]
            if user_to_rep.id != message.author.id:  # Проверяем, чтобы пользователь не добавил репутацию сам себе
                try:
                    if not self.db.check_reputation(message.author.id, user_to_rep.id):  # Проверяем, можно ли добавить репутацию
                        await self.add_reputation(user_to_rep, message.channel)
                    else:
                        await message.channel.send("Вы уже добавляли репутацию этому пользователю!")
                except Exception as e:
                    await message.channel.send(f"Произошла ошибка при добавлении репутации: {e}")
            else:
                await message.channel.send("Вы не можете добавить репутацию самому себе!")

    async def add_reputation(self, user, channel):
        # Посылка сообщения о добавлении репутации
        if channel:
            await channel.send(f"Репутация пользователя {user.display_name} увеличена на +1!")

        # Обновление репутации в базе данных
        try:
            self.db.update_reputation(user.id, 1)
        except Exception as e:
            await channel.send(f"Произошла ошибка при обновлении репутации: {e}")

def setup(bot):
    from db_connect import Database  # Импорт вашего модуля управления базой данных
    db = Database()  # Создаем экземпляр класса базы данных
    try:
        db.connect()  # Устанавливаем соединение с базой данных
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    bot.add_cog(Reputation(bot, db))  # Добавляем ког, передавая экземпляр базы данных
