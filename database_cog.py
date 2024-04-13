import disnake
from disnake.ext import commands
from db_connect import Database

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.db.connect()

    def cog_unload(self):
        self.db.disconnect()
        print("Ког выгружен. Соединение с базой данных закрыто.")

def setup(bot):
    bot.add_cog(DatabaseCog(bot))
