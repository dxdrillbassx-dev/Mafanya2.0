import disnake
from disnake.ext import commands
from discord.ext import tasks

class SpotifyStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.track_url = None

    @tasks.loop(seconds=30)  # Период обновления статуса (в секундах)
    async def update_status(self):
        if self.track_url:
            activity_name = f"Spotify: {self.track_url}"
        else:
            activity_name = "nothing on Spotify"
        await self.bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.listening,
                name=activity_name
            )
        )

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def set_spotify_track(self, ctx, track_url: str):
        self.track_url = track_url
        await ctx.send("The Spotify track URL has been successfully set.")

def setup(bot):
    bot.add_cog(SpotifyStatus(bot))
