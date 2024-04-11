from disnake.ext import commands

CENSORED_WORDS = ['блять', 'сука']  # Список цензуры

class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for content in message.content.split():
            for censored_word in CENSORED_WORDS:
                if content.lower() == censored_word:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} такие слова запрещены!")

