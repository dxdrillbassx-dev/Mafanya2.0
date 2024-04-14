from disnake.ext import commands

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calc", description="Простой калькулятор")
    async def calc(self, ctx, a: int, oper: str, b: int):
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

        await ctx.send(str(result))