import disnake
from disnake.ext import commands
import re

class CapsFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.caps_filter_enabled = False

    async def cog_check(self, ctx):
        # Проверяем, является ли автор команды администратором
        return ctx.author.permissions_in(ctx.channel).administrator

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.caps_filter_enabled:
            return

        # Проверка наличия капса в сообщении
        if re.search(r'[A-Z]{5,}', message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} Включен капс-фильтр, поэтому пиши адекватно :D", delete_after=10)

    @commands.slash_command(description="Включить фильтр капса")
    async def enable_caps_filter(self, ctx):
        if self.caps_filter_enabled:
            await ctx.send("Фильтр капса уже включен.")
        else:
            self.caps_filter_enabled = True
            await ctx.send("Фильтр капса включен, перестаем повышать буквы.")

    @commands.slash_command(description="Выключить фильтр капса")
    async def disable_caps_filter(self, ctx):
        if not self.caps_filter_enabled:
            await ctx.send("Фильтр капса уже выключен.")
        else:
            self.caps_filter_enabled = False
            await ctx.send("Фильтр капса выключен, можно снова повышать буквы.")

def setup(bot):
    bot.add_cog(CapsFilter(bot))
