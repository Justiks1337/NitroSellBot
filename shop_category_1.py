import disnake
from changing_balance import withdrawal_of_funds
from DataBaseAssistant import change, select
from profile_info import on_buy_event


products = {"Nitro_1month": 100}


class CategoryMenu(disnake.ui.Select):
    def __init__(self, values):
        super().__init__(placeholder="Select an option", max_values=1, min_values=1)
        for i in values:
            self.add_option(label=i[1], description="Товар")

    async def callback(self, inter):
        await inter.response.edit_message(embed=disnake.Embed(description="Ты уверен что хочешь купить этот товар? \n 1. *Перед покупкой начни запись для отката (на всякий случай)* \n *Используй ВПН для активации (если в России)* \n *Принятие в течении 10 минут*"), view=NitroBuyButtons(self.values))


class CategoryView(disnake.ui.View):
    def __init__(self, values):
        super().__init__()
        self.add_item(CategoryMenu(values))

    @disnake.ui.button(custom_id="Back", emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, row=2)
    async def back_button_callback(self, button, inter):
        pass


class NitroBuyButtons(disnake.ui.View):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @disnake.ui.button(label="Да. Купить", emoji="✅", custom_id="buy_nitro", style=disnake.ButtonStyle.success)
    async def buy_confirm_button_callback(self, button, inter):
        price = await select("SELECT price FROM products WHERE name = ?", (self.name[0],))
        await withdrawal_of_funds(inter, price[0])
        await on_buy_event(self.name[0], inter, price[0])
        id = await select("SELECT id FROM products WHERE name = ?", (self.name[0],))
        product = await select("SELECT token FROM tokens WHERE id = ?", (id[0], ))
        await inter.response.edit_message(f"Поздравляем вас с покупкой, вот ваш товар: \n \n {product[0]}", embed=None, view=None)
        await change("DELETE FROM tokens WHERE token = ?", (product[0], ))

    @disnake.ui.button(custom_id="Back", emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray)
    async def back_button_callback(self, button, inter):
        pass

    async def on_error(self, error, item, inter):
        pass


