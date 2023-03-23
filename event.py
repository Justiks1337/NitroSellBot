import disnake
from disnake.ext import commands
from start_menu import show_menu
from admin_panel import show_admin_menu


class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "Back":
            await show_menu(inter)
        elif inter.component.custom_id == "admin_panel":
            await show_admin_menu(inter)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await inter.response.send_message(embed=disnake.Embed(description="**Данную команду разрешено отправлять только в личные сообщения бота в целях безопасности ваших данных!**").set_author(name="Сударь! ❌"), ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Event(bot))
