import disnake
from random import getrandbits
from changing_balance import replenishment_of_funds, withdrawal_of_funds

multiplier = 1.2  # Можешь заменить если хочешь сделать умножение балика меньше/больше (не советую, подобрано идеальное значение
CoinFrame = disnake.Embed(title="Монетка", description=f"Множитель {multiplier} \n Твоя задача выбрать одну из сторон монетки, если угадываешь - умножаешь свою ставку на множитель").add_field(value=str(3), name="Ставка")


class CoinButtons(disnake.ui.View):
    @disnake.ui.button(label="Орёл", emoji="🪙", style=disnake.ButtonStyle.primary)
    async def orel_button_callback(self, button, inter):
        await withdrawal_of_funds(inter, int(inter.message.embeds[0].fields[0].value))
        if bool(getrandbits(1)):
            await replenishment_of_funds(inter, round(int(inter.message.embeds[0].fields[0].value) * multiplier, 1))
            await inter.send(embed=disnake.Embed(description=f"Ты успешно выиграл {str(round(int(inter.message.embeds[0].fields[0].value) * multiplier, 1))} монет!"), ephemeral=True)
            return
        await inter.send(embed=disnake.Embed(description=f"Ты проиграл {inter.message.embeds[0].fields[0].value} монет!"), ephemeral=True)

    @disnake.ui.button(label="Решка", emoji="🪙", style=disnake.ButtonStyle.primary)
    async def reshka_button_callback(self, button, inter):
        await withdrawal_of_funds(inter, int(inter.message.embeds[0].fields[0].value))
        if not bool(getrandbits(1)):
            await replenishment_of_funds(inter, round(int(inter.message.embeds[0].fields[0].value) * multiplier, 1))
            await inter.send(embed=disnake.Embed(description=f"Ты успешно выиграл {str(round(int(inter.message.embeds[0].fields[0].value) * multiplier, 1))} монет!"), ephemeral=True)
            return
        await inter.send(embed=disnake.Embed(description=f"Ты проиграл {inter.message.embeds[0].fields[0].value} монет!"), ephemeral=True)

    @disnake.ui.button(label="Изменить ставку", emoji="💠", style=disnake.ButtonStyle.success, row=2)
    async def change_bit_button_callback(self, button, inter):
        await inter.response.send_modal(modal=InputBit())

    @disnake.ui.button(label="Вернуться", emoji="👈", custom_id="Back", style=disnake.ButtonStyle.gray)
    async def back_button_callback(self, button, inter):
        pass

    async def on_error(self, error, item, inter):
        pass


class InputBit(disnake.ui.Modal):
    """
    Класс  InputBit отвечает за модальное окно для ввода в него значения.

    Используется в coin.py

    Наследуется от disnake.ui.Modal
    """
    def __init__(self):
        components = [disnake.ui.TextInput(label="Ставка", placeholder="Введите свою ставку", custom_id="bit", style=disnake.TextInputStyle.short, max_length=50,)]
        super().__init__(title="Create Tag", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            check = int(inter.text_values["bit"])
            if check > 3:
                await inter.response.edit_message(embed=CoinFrame.set_field_at(index=0, value=str(check), name="Ставка"))
                return
            await inter.send(embed=disnake.Embed(description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), ephemeral=True)
        except ValueError:
            await inter.send(embed=disnake.Embed(description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), ephemeral=True)


async def show_coin(inter):
    await inter.response.edit_message(embed=CoinFrame, view=CoinButtons(timeout=None))
