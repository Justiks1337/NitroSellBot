from start_menu import show_menu
from disnake.ext import commands


class StartCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    @commands.dm_only()
    async def start(self, inter):
        await show_menu(inter)


def setup(bot: commands.Bot):
    bot.add_cog(StartCommand(bot))
