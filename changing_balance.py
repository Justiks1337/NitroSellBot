from sys import exit as ex

import disnake
from DataBaseAssistant import change, select


async def withdrawal_of_funds(inter, price):
    """Сопрограмма withdrawal_of_funds отвечает за списание средств со счёта пользователя

        Принимает в себя:
        inter - disnake.Interaction
        price - стоимость товара

        Возвращает:
            Null
    """
    balance = await select("SELECT balance FROM users WHERE id = ?", (inter.author.id, ))
    if balance[0] - price >= 0:
        await change("UPDATE users SET balance = ? WHERE id=?", (balance[0]-price, inter.author.id))
        return
    await inter.response.send_message(embed=disnake.Embed(description="**Не достаточно средств на балансе!** :x:"), ephemeral=True)
    raise ZeroDivisionError()


async def replenishment_of_funds(inter, amount):
    """Сопрограмма withdrawal_of_funds отвечает за списание средств со счёта пользователя

        Принимает в себя:
        inter - disnake.Interaction
        price - надбавка к балансу

        Возвращает:
            Null
    """
    balance = await select("SELECT balance FROM users WHERE id = ?", (inter.author.id, ))
    await change("UPDATE users SET balance = ? WHERE id=?", (balance[0]+amount, inter.author.id))
