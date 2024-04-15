import disnake
from disnake.ext import commands

class Reputation(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.bot.user:
            return

        if message.content.startswith('+') and message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message.author == message.author:
                await message.channel.send("Вы не можете добавить репутацию самому себе!")
                return

        if message.content.startswith('+') and message.mentions:
            user_to_rep = message.mentions[0]
            if user_to_rep.id != message.author.id:  # Проверка на разных пользователей
                try:
                    if not self.db.check_reputation(message.author.id, user_to_rep.id):
                        await self.add_reputation(message, user_to_rep)
                    else:
                        await message.channel.send("Вы уже добавляли репутацию этому пользователю!")
                except Exception as e:
                    await message.channel.send(f"Произошла ошибка при добавлении репутации: {e}")

    async def add_reputation(self, message, user):
        channel = message.channel
        if channel:
            await channel.send(f"Репутация пользователя {user.display_name} увеличена на +1!")
        try:
            self.db.add_reputation(message.author.id, user.id, 1)
        except Exception as e:
            await message.channel.send(f"Произошла ошибка при обновлении репутации: {e}")

def setup(bot):
    from db_connect import Database
    db = Database()
    try:
        db.connect()
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    bot.add_cog(Reputation(bot, db))
