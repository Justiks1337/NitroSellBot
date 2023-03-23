import requests
from asyncio import sleep
from config import settings


pay_requestions = {}  # Словарь для хранения bill


async def create_p2p_bill(user_id, amount):
    """
        Асинхронная функция create_p2p_bill создаёт новую форму оплаты на платформе RuKassa
            Добавляет в словарь main.py/pay_requestions новый объект оплаты для дальнейшего использования
            В сопрограммах: checking_activity_request.

        Принимает в себя:
            user_id - ID пользователя проводящего оплату
            amount - Сумма пополнения

        Примечание:
            Переписан с Qiwi -> YouKassa -> RuKassa
    """
    response = requests.post("https://lk.rukassa.pro/api/v1/create", {
        'shop_id': settings['rukassa_shop_id'],
        'order_id': len(pay_requestions) + 1,
        'amount': float(amount),
        'token': settings['secret_rukassa_key']})
    print(response.json())
    pay_requestions[user_id] = response.json()


async def checking_activity_request(user_id):
    """
        Асинхронная функция checking_activity_request возвращает значение
            Используется в сопрограммах delete_inactive_requests и по нажатию кнопки "Проверить оплату"

        Принимает в себя:
            user_id - ID пользователя совершающего проверку оплаты

        Возвращает:
            Статус оплаты.
    """
    response = requests.get('https://lk.rukassa.pro/api/v1/getPayInfo', {
        'id': pay_requestions[user_id]['id'],
        'shop_id': settings['rukassa_shop_id'],
        'token': settings['secret_rukassa_key']
    })
    return response.json()['status']


async def delete_inactive_requests():
    """
        Асинхронная функция delete_inactive_requests удаляет из словаря pay_requestions все истёкшие запросы оплаты
            Используется в сопрограммах: while_deletion_bill

        Ничего не принимает в себя и не возвращает.

    """
    for i in pay_requestions.copy():
        if await checking_activity_request(i) == "CANCEL":
            del pay_requestions[i]


async def while_deletion_bill(time):
    """
        Асинхронная функция while_deletion_bill бесконечно воспроизводит сопрограмму delete_inactive_requests()
        Один раз в указанное время в аргументе time.

        Принимает:
            time - INT (время указать в секундах)

        Ничего не возвращает.

        Примечание:
            Автор знает про понятие рекурсивных функций, но не использует
            Т.к. у рекурсивных функций есть ограничения.
    """
    while True:
        await delete_inactive_requests()
        await sleep(time)
