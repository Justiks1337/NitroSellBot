from glQiwiApi import QiwiP2PClient, QiwiWrapper
from asyncio import sleep
import datetime
from config import settings


pay_requestions = {}  # Словарь для хранения bill


async def expire_at(time):
    """
    Асинхронная функция expire_at возвращает время окончания действия ссылки на оплату
        Используется в сопрограммах: create_p2p_bill


    :param time: Время действие ссылки на форму
    :return: Время окончания действия ссылки
    """

    return datetime.datetime.now() + datetime.timedelta(minutes=time)


async def delete_the_second_form_of_payment(user_id):
    async with QiwiP2PClient(secret_p2p=settings['secret_qiwi_key']) as p2p:
        if user_id in pay_requestions:
            await p2p.reject_p2p_bill(bill_id=pay_requestions[user_id].id)
            del pay_requestions[user_id]


async def create_p2p_bill(user_id, amount):
    """
        Асинхронная функция create_p2p_bill создаёт новую форму оплаты на платформе Qiwi
            Добавляет в словарь main.py/pay_requestions новый объект оплаты для дальнейшего использования
            В сопрограммах: checking_activity_request.

        Принимает в себя:
            user_id - ID пользователя проводящего оплату
            amount - Сумма пополнения
    """
    async with QiwiP2PClient(secret_p2p=settings['secret_qiwi_key']) as p2p:
        await delete_the_second_form_of_payment(user_id)
        bill = await p2p.create_p2p_bill(amount=amount, expire_at=await expire_at(10))
        pay_requestions[user_id] = bill


async def checking_activity_request(user_id):
    """
        Асинхронная функция checking_activity_request возвращает значение
            Используется в сопрограммах delete_inactive_requests и по нажатию кнопки "Проверить оплату"

        Принимает в себя:
            user_id - ID пользователя совершающего проверку оплаты

        Возвращает:
            Статус оплаты.
    """
    async with QiwiWrapper(secret_p2p=settings['secret_qiwi_key']) as w:
        return await w.check_p2p_bill_status(bill_id=pay_requestions[user_id].id)


async def delete_inactive_requests():
    """
        Асинхронная функция delete_inactive_requests удаляет из словаря pay_requestions все истёкшие запросы оплаты
            Используется в сопрограммах: while_deletion_bill

        Ничего не принимает в себя и не возвращает.

    """
    for i in pay_requestions.copy():
        if await checking_activity_request(i) == "EXPIRED":
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
