import disnake
from disnake.ext import commands
from DataBaseAssistant import select, change


class BalanceManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def add_money(self, inter, member: disnake.Member, amount: int):
        balance = await select("SELECT balance FROM users WHERE id = ?", (member.id,))
        await change("UPDATE users SET balance = ? WHERE id=?", (balance[0] + amount, member.id))
        await inter.response.send_message(embed=disnake.Embed(description=f"**Вы успешно пополнили баланс пользователя {member}** :white_check_mark:"))

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def remove_money(self, inter, member: disnake.Member, price: int):
        balance = await select("SELECT balance FROM users WHERE id = ?", (member.id,))
        if balance[0] - price >= 0:
            await change("UPDATE users SET balance = ? WHERE id=?", (balance[0] - price, member.id))
            await inter.response.send_message(embed=disnake.Embed(description=f"**Вы успешно уменьшили баланс {member}** :white_check_mark:"))
            return
        await inter.response.send_message(embed=disnake.Embed(description=f"**Не достаточно средств на балансе пользователя {member}** :x:"), ephemeral=True)
        return


def setup(bot: commands.Bot):
    bot.add_cog(BalanceManagement(bot))