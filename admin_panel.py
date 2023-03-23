import disnake
from DataBaseAssistant import change, full_select
from disnake import TextInputStyle


class AdminPanelView(disnake.ui.View):
    @disnake.ui.button(label="Создать новый товар", emoji="➕", style=disnake.ButtonStyle.primary, custom_id="create_new_product")
    async def create_new_product_button_callback(self, button, inter):
        await inter.response.send_message(embed=disnake.Embed(description="Выбери категорию в которую хочешь добавить товар"), view=CategoryMenuView())

    @disnake.ui.button(label="Удалить товар", emoji="➖", style=disnake.ButtonStyle.primary, custom_id="delete_product")
    async def delete_product_button_callback(self, button, inter):
        await inter.response.send_modal(InputDeleteProduct())

    @disnake.ui.button(label="Изменить товар", emoji="⏮️", style=disnake.ButtonStyle.primary, custom_id="change_product")
    async def change_product_button_callback(self, button, inter):
        await inter.response.send_modal(InputEditProduct())

    @disnake.ui.button(custom_id="Back", emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray)
    async def back_button_callback(self, button, inter):
        pass


async def show_admin_menu(inter):
    show_products = "" #админ надристал говнокода
    products = await full_select("SELECT * FROM products")
    for i in await products.fetchall():
        show_products = show_products + str(i) + '\n'
    await inter.response.edit_message(embed=disnake.Embed(title="Список товаров", description=show_products), view=AdminPanelView())


class InputNewProduct(disnake.ui.Modal):
    """
    Класс InputNewProduct отвечает за модальное окно для ввода в него значения.

    Используется в admin_panel/create_new_product_button_callback

    Наследуется от disnake.ui.Modal
    """
    def __init__(self, category):
        self.category = category
        components = [disnake.ui.TextInput(label="Название товара", placeholder="Введите название товара", custom_id="product_name", style=TextInputStyle.short, max_length=100,), disnake.ui.TextInput(label="Цена товара", placeholder="Введите цену товара", custom_id="product_price", style=TextInputStyle.short, max_length=100,)]
        super().__init__(title="Create Tag", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        await add_new_product(inter, self.category)


class CategoryMenu(disnake.ui.Select):
    def __init__(self):
        options = [
                disnake.SelectOption(label="Discord", emoji="👌", description="без гарантии"),
                disnake.SelectOption(label="Telegram", emoji="👌", description="без гарантии"),
                disnake.SelectOption(label="Minecraft", emoji="👌", description="без гарантии"),
                disnake.SelectOption(label="Прочее", emoji="👌", description="без гарантии"),
            ]
        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, inter):
        if self.values[0] == "Discord":
            await inter.response.send_modal(InputNewProduct(1))
        elif self.values[0] == "Telegram":
            await inter.response.send_modal(InputNewProduct(2))
        elif self.values[0] == "Minecraft":
            await inter.response.send_modal(InputNewProduct(3))
        elif self.values[0] == "Прочее":
            await inter.response.send_modal(InputNewProduct(4))


class CategoryMenuView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CategoryMenu())

    @disnake.ui.button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back", row=2)
    async def back_button_callback(self, button, inter):
        pass


async def add_new_product(inter, category):
    await change("INSERT INTO products VALUES (?, ?, ?, ?)", (None, inter.text_values["product_name"], inter.text_values["product_price"], category))
    await inter.response.send_message(embed=disnake.Embed(description="Ты успешно создал новый товар!"), ephemeral=True)


class InputDeleteProduct(disnake.ui.Modal):
    """
    Класс InputNewProduct отвечает за модальное окно для ввода в него значения.

    Используется в admin_panel/delete_product_button_callback

    Наследуется от disnake.ui.Modal
    """
    def __init__(self):
        components = [disnake.ui.TextInput(label="id товара", placeholder="Введите id товара", custom_id="product_id", style=TextInputStyle.short, max_length=100)]
        super().__init__(title="Create Tag", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        await change("DELETE FROM products WHERE id = ?", (inter.text_values["product_id"], ))
        await inter.response.send_message(embed=disnake.Embed(description="*Товар успешно удалён*"), ephemeral=True)


class InputEditProduct(disnake.ui.Modal):
    """
    Класс InputEditProduct отвечает за модальное окно для ввода в него значения.

    Используется в admin_panel/change_product_button_callback

    Наследуется от disnake.ui.Modal
    """
    def __init__(self):
        components = [disnake.ui.TextInput(label="id товара", placeholder="Введите id товара", custom_id="product_id", style=TextInputStyle.short, max_length=100), disnake.ui.TextInput(label="Название товара", placeholder="Введите название товара", custom_id="product_name", style=TextInputStyle.short, max_length=100,), disnake.ui.TextInput(label="Цена товара", placeholder="Введите цену товара", custom_id="product_price", style=TextInputStyle.short, max_length=100,)]
        super().__init__(title="Введите новые значения", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        await change("UPDATE products SET name = ?, price = ? WHERE id = ? ", (inter.text_values["product_name"], inter.text_values["product_price"], inter.text_values["product_id"]))
        await inter.response.send_message(embed=disnake.Embed(description="*Товар успешно изменён*"), ephemeral=True)