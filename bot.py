import disnake
from disnake.ext import commands
from censorship import Censorship
from welcome import Welcome
from moderation import Moderation
from calc import Calculator
from rules_menu import RulesMenu
from party import Party
from menu import Menu
from economy_cog import Economy
from profile_cog import ProfileView
from profile_cog import Profile
from db_connect import Database

bot = commands.Bot(command_prefix=commands.when_mentioned, help_command=None, intents=disnake.Intents.all(), test_guilds=[1227760104963837952])
bot.db = Database()
bot.db.connect()
bot.db.create_tables()

# Загрузка модулей (cogs)
bot.add_cog(Censorship(bot))
bot.add_cog(Welcome(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Calculator(bot))
bot.add_cog(RulesMenu(bot))
bot.add_cog(Party(bot))
bot.add_cog(Menu(bot))
bot.add_cog(Economy(bot))

bot.load_extension("profile_cog")
bot.load_extension("database_cog")

@bot.event
async def on_ready():
    print(f"- [Mafanya] Я {bot.user} полностью готова к работе.")

@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f"Правильное использование команды: {ctx.prefix}{ctx.command.name}\nПример: {ctx.prefix}{ctx.command.usage}"
        ))

# Токен
bot.run('MTIyNjkzNzYwMjY2NjQwMTgxMg.G0VaZu.nik9AnmESFU5gif3hXR2Mmk4LFH3sDTeFFG_IM')

