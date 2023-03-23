import disnake
from shop_category_1 import CategoryView
from DataBaseAssistant import unfull_select, full_select


class ShopSelectMenu(disnake.ui.Select):
    def __init__(self):
        options = [
                disnake.SelectOption(label="Discord", emoji="✨", description="Список товаров"),
                disnake.SelectOption(label="Telegram", emoji="✨", description="Список товаров"),
                disnake.SelectOption(label="Minecraft", emoji="✨", description="Список товаров"),
                disnake.SelectOption(label="Прочее", emoji="✨", description="Список товаров"),
            ]
        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, inter):
        try:
            if self.values[0] == "Discord":
                my_select = await unfull_select("SELECT * FROM products WHERE category = ?", (1,))
                await inter.response.edit_message(embed=disnake.Embed(description=await give_message(my_select)), view=CategoryView(my_select))
            elif self.values[0] == "Telegram":
                my_select = await unfull_select("SELECT * FROM products WHERE category = ?", (2,))
                await inter.response.edit_message(embed=disnake.Embed(description=await give_message(my_select)), view=CategoryView(my_select))
            elif self.values[0] == "Minecraft":
                my_select = await unfull_select("SELECT * FROM products WHERE category = ?", (3,))
                await inter.response.edit_message(embed=disnake.Embed(description=await give_message(my_select)), view=CategoryView(my_select))
            elif self.values[0] == "Прочее":
                my_select = await unfull_select("SELECT * FROM products WHERE category = ?", (4,))
                await inter.response.edit_message(embed=disnake.Embed(description=await give_message(my_select)), view=CategoryView(my_select))
        except:
            await inter.response.edit_message(embed=disnake.Embed(description="Товар soon..."), components=[disnake.ui.Button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back")])


class ShopView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ShopSelectMenu())

    @disnake.ui.button(emoji="👈", label="Вернуться", style=disnake.ButtonStyle.gray, custom_id="Back", row=2)
    async def back_button_callback(self, button, inter):
        """
        На заметку
        Автор знает этот метод пустой, он был создан что бы не отходить от концепции создания кнопок через методы
        Автор знает что кнопку можно добавить через View.add_item
        Если автору метода захочется исключить этот метод из кода - он это сделает
        """
        pass


async def give_message(my_select):
    message = ""
    for i in my_select:
        products = await unfull_select("SELECT token FROM tokens WHERE id = ?", (i[0], ))
        message = message + f"**{i[1]}** \n Цена товара: {i[2]} \n Сейчас на складе: {len(products)} \n"
    return message
