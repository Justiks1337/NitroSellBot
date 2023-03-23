import disnake
from payment_menu import InputAmount
from profile_info import get_info


class ProfileButtons(disnake.ui.View):
    """
    Класс ProfileButtons отвечает за отображение и отклик кнопок в меню профиля
    Наследуется от класса disnake.ui.View
    """
    @disnake.ui.button(emoji="💰", label="Пополнить баланс", style=disnake.ButtonStyle.green, custom_id="add_money")
    async def addmoney_button_callback(self, button, inter):
        await inter.response.send_modal(modal=InputAmount())

    @disnake.ui.button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back")
    async def back_button_callback(self, button, inter):
        """
        На заметку
        Автор знает этот метод пустой, он был создан что бы не отходить от концепции создания кнопок через методы
        Автор знает что кнопку можно добавить через View.add_item
        Если автору метода захочется исключить этот метод из кода - он это сделает
        """
        pass


async def show_profile(inter):
    info = await get_info(inter)
    await inter.response.edit_message(embed=disnake.Embed(description=f"Баланс: \n `{info[0]} Р💸` \n \n Куплено товаров: \n `{info[1]} шт.` \n \n Потрачено монет: \n `{info[2]} Р💸`", ).set_author(name=f"Твой профиль ({inter.author})").set_thumbnail(url=inter.author.avatar), view=ProfileButtons())
