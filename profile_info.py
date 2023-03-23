from DataBaseAssistant import change, select
import disnake
from config import settings


async def get_info(inter):
    info = await select("SELECT balance, buy_products, spent_money FROM users WHERE id = ?", (inter.author.id,))
    if not info[1]:
        await change("REPLACE INTO users VALUES (?, ?, ?, ?)", (inter.author.id, 0, 0, 0))
        info = (0, 0, 0)
    return info


async def on_buy_event(product, inter, price):
    info = await select("SELECT buy_products, spent_money FROM users WHERE id = ?", (inter.author.id, ))
    await change("UPDATE users SET buy_products = ?, spent_money = ? WHERE id = ?", (info[0] + 1, info[1] + price, inter.author.id))
    admin = inter.client.get_user(settings['admin_id'][0])
    await admin.send(embed=disnake.Embed(description=f'{inter.author} \n Товар: {product} \n Цена: {price}', color=disnake.Color.red(), title='Оповещение о покупке товара'))
