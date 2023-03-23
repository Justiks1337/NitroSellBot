import disnake
from random import randint
from changing_balance import replenishment_of_funds, withdrawal_of_funds


class CaseButtons(disnake.ui.View):
    @disnake.ui.button(label="Открыть кейс (10 рублей)", emoji="👐", custom_id="open_case", style=disnake.ButtonStyle.success)
    async def open_case_button_callback(self, button, inter):
        await open_case(inter)

    @disnake.ui.button(label="Вернуться", emoji="👈", custom_id="Back", style=disnake.ButtonStyle.primary)
    async def back_button_callback(self, button, inter):
        pass

    async def on_error(self, error, item, inter):
        pass


class ReopenCaseButtons(disnake.ui.View):
    @disnake.ui.button(label="Вернуться", emoji="👈", custom_id="Back_to_case", style=disnake.ButtonStyle.gray)
    async def back_to_case_button_callback(self, button, inter):
        await inter.response.edit_message(embed=disnake.Embed(description="Для открытия кейса нажми на \"Открыть кейс\" \n **В кейсах большие шансы на выигрыш!**"), view=CaseButtons())


async def open_case(inter):
    await withdrawal_of_funds(inter, 10)
    for i in range(5):
        rnd_int = randint(0, 15)
        await inter.message.edit(embed=disnake.Embed(title="Открытие кейса...", description=f"**Происходит открытие кейса, ожидайте появления результатов... \n ======={rnd_int}======**"))
    await replenishment_of_funds(inter, rnd_int)
    await inter.response.edit_message(embed=disnake.Embed(title="Кейс успешно открыт!", description=f"Ваш выигрыш составляет {rnd_int}:money_with_wings:"), view=ReopenCaseButtons())
