import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all(), test_guilds=[1227760104963837952])

CENSORED_WORDS = ['блять', 'сука']

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work.")

@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id=1227772107312595055)
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
    await bot.process_commands(message)

    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                await message.delete()
                await message.channel.send(f"{message.author.mention} такие слова запрещены!")

@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}`\nExample: {ctx.prefix}{ctx.command.usage}"
        ))

@bot.command(name="кик", aliases=["кыш", "выгнать"], usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил!"):
    await ctx.send(f"Администратор {ctx.author.mention} исключил пользователя {member.mention}")
    await member.kick(reason=reason)
    await ctx.message.delete()

@bot.command(name="бан", aliases=["баня", "банан"], usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил!"):
    await ctx.send(f"Администратор {ctx.author.mention} забанил пользователя {member.mention}")
    await member.ban(reason=reason)
    await ctx.message.delete()

@bot.slash_command(description="Обычный, простой калькулятор:)")
async def calc(inter, a: int, oper: str, b: int):
    if oper == "+":
        result = a + b
    elif oper == "-":
        result = a - b
    elif oper == "*":
        result = a * b
    elif oper == "/":
        result = a / b
    else:
        result = "Неверный оператор!"

    await inter.send(str(result))

bot.run('MTIyNjkzNzYwMjY2NjQwMTgxMg.G0VaZu.nik9AnmESFU5gif3hXR2Mmk4LFH3sDTeFFG_IM')