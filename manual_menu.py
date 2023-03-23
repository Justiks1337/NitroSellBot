import disnake


MANUAL = disnake.Embed(description="*Шаг 1:* \n В стартовом меню нажми на кнопку Профиль. \n *Шаг 2:* \n В выпавшем меню нажми на кнопку пополнить баланс. \n *Шаг 3:* \n В выпавшем окне введи сумму на которую хочешь пополнить баланс, и оплати. \n *Шаг 4:* \n После оплаты нажми на кнопку Проверить оплату. Если оплата прошла успешно, на твой баланс зачислятся деньги. \n *Шаг 5:* \n В основном меню нажми на кнопку Магазин и выбери интересующий тебя товар. Далее следуй по иструкциям приложенным к товару \n \n В любой не понятной ситуации (не валид ссылка) писать antioch#9999 \n **Удачи!**")


async def show_manual(inter):
    """ Сопрограмма show_manual отвечает за вывод инструкци

        Используется в start_menu/manual_button_callback

        Принимает inter
    """
    await inter.response.edit_message(embed=MANUAL.set_author(name="Инструкция"), components=[disnake.ui.Button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back")])
