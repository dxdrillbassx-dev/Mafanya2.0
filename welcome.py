from disnake.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(1227772107312595055)
        channel = member.guild.system_channel

        embed = disnake.Embed(
            title="Новый участник!",
            description=f"{member.name}#{member.discriminator}",
            color=0xffffff
        )

        await member.add_roles(role)
        await channel.send(embed=embed)

