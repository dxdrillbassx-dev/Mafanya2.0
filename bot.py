import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all())

CENSORED_WORDS = ['блять', 'сука']

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work.")

@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id=1227763641747640464)
    channel = member.guild.system_channel

    embed = disnake.Embed(
        title="Новый участник!",
        description=f"{member.name}#{member.discriminator}",
        color=0xffffff
    )

    await member.add_roles(role)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                await message.delete()
                await message.channel.send(f"{message.author.mention} такие слова запрещены!")

@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил!"):
    await ctx.send(f"Администратор {ctx.author.mention} исключил пользователя {member.mention}", delete_after=2)
    await member.kick(reason=reason)
    await ctx.message.delete()

bot.run('MTIyNjkzNzYwMjY2NjQwMTgxMg.G0VaZu.nik9AnmESFU5gif3hXR2Mmk4LFH3sDTeFFG_IM')