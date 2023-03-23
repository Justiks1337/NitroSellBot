import disnake
from disnake import TextInputStyle
from PaymentSystem import create_p2p_bill, pay_requestions, checking_activity_request
from changing_balance import replenishment_of_funds
from glQiwiApi.qiwi.exceptions import ValidationError


class PaymentMenuButtons(disnake.ui.View):
    """
        Класс PaymentMenuButtons отвечает за отображение и отклик кнопок в меню оплаты
        Наследуется от класса disnake.ui.View
    """
    @disnake.ui.button(emoji="♻️", label="Проверить оплату", style=disnake.ButtonStyle.blurple, custom_id="check")
    async def checkpay_button_callback(self, button, inter):
        request = await checking_activity_request(inter.author.id)
        if request == "WAITING":
            await inter.response.send_message(embed=disnake.Embed(description=":x: \n \n **Оплата ещё не прошла. Если вы оплатили, но видите это сообщение подождите несколько минут, перед тем как писать в поддержку.**"), ephemeral=True)
            return
        elif request == "PAID":
            await replenishment_of_funds(inter, pay_requestions[inter.author.id].amount.value)
            await inter.response.edit_message(embed=disnake.Embed(description=":white_check_mark: \n \n**Оплата прошла успешно! Огромное спасибо за оплату**"), component=disnake.ui.Button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back"))
            del pay_requestions[inter.author.id]
            return


class InputAmount(disnake.ui.Modal):
    """
    Класс MyModal отвечает за модальное окно для ввода в него значения.

    Используется в ProfileButtons/addmoney_button_callback

    Наследуется от disnake.ui.Modal
    """
    def __init__(self):
        components = [disnake.ui.TextInput(label="Сумма пополнения", placeholder="Введите сумму пополнения", custom_id="amount", style=TextInputStyle.short, max_length=50,)]
        super().__init__(title="Create Tag", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            check = int(inter.text_values["amount"])
            if check > 3:
                await create_p2p_bill(inter.author.id, inter.text_values["amount"])
                await inter.response.edit_message(embed=disnake.Embed(description="***Для оплаты нажми на кнопку Оплатить. На открывшемся сайте оплатите покупку, после оплаты нажмите кнопку Проверить оплату***"), view=PaymentMenuButtons(timeout=600.0).add_item(item=disnake.ui.Button(emoji="💠", label="Оплатить", style=disnake.ButtonStyle.url, url=pay_requestions[inter.author.id].pay_url)))
                return
            await inter.send(embed=disnake.Embed(description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), ephemeral=True)

        except ValidationError:
            await inter.send(embed=disnake.Embed(description="Вы ввели слишком большое число"))
        except ValueError:
            await inter.send(embed=disnake.Embed(description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), ephemeral=True)

