import disnake
from manual_menu import show_manual
from profile_menu import show_profile
from shop_menu import ShopView
from casino import CasinoView
from config import settings


START_MENU = disnake.Embed(description="**Приветствую!** \n \n *Куда направимся сейчас?*").set_thumbnail(url="https://media.discordapp.net/attachments/1072169416898379817/1078611520184930355/logo2_static.png")  # Сообщение отображающее стартовое меню


class StartMenuButtons(disnake.ui.View):
    """
    Класс StartMenuButtons отвечает за кнопки и их действия

    Наследован от класса Viev.
                                                            """
    @disnake.ui.button(emoji="📕", label="Профиль", style=disnake.ButtonStyle.gray, custom_id="profile")
    async def profile_button_callback(self, button, inter):
        await show_profile(inter)

    @disnake.ui.button(emoji="🛒", label="Магазин", style=disnake.ButtonStyle.success, custom_id="shop")
    async def shop_button_callback(self, button, inter):
        await inter.response.send_message(embed=disnake.Embed(description="*Выбери товар который хочешь купить*"), view=ShopView())

    @disnake.ui.button(emoji="🎮", label="Казино", style=disnake.ButtonStyle.red, custom_id="open_casino_menu")
    async def casino_button_callback(self, button, inter):
        await inter.response.edit_message(embed=disnake.Embed(title="Казино", description="*Выбери игру в которую хочешь сыграть*"), view=CasinoView())

    @disnake.ui.button(emoji="🔍", label="Инструкция", style=disnake.ButtonStyle.primary, custom_id="Help")
    async def manual_button_callback(self, button, inter):
        await show_manual(inter)


async def show_menu(inter):
    """ Сопрограмма show_menu отвечает за отображение меню.
        Используется в start_cog.py/start

        Принимает inter.
                                      """
    if inter.author.id in settings['admin_id']:
        await inter.response.send_message(embed=START_MENU, view=StartMenuButtons().add_item(disnake.ui.Button(label="Админ-панель", emoji="✖️", custom_id="admin_panel", style=disnake.ButtonStyle.red)))
        return
    await inter.response.send_message(embed=START_MENU, view=StartMenuButtons())
