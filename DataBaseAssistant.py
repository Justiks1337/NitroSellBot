from DataBaseConnector import db
import aiosqlite
from asyncio import sleep
from YandexDBBackuper import backuper


transaction = 0  # Совершено транзакций от последнего бекапа бд

amount_transaction = 2 # Кол-во транзакций для бекапа бд


async def select(my_select, values):
    for i in range(3):
        try:
            sql = await db.cursor()
            found = await sql.execute(my_select, values)
            return await found.fetchone()

        except aiosqlite.ProgrammingError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("ProgrammingError")
            await sleep(3)

        except aiosqlite.OperationalError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("OperationalError")
            await sleep(3)

        except aiosqlite.NotSupportedError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("NotSupportedError")
            await sleep(3)


async def change(my_changes, values):
    for i in range(3):
        try:
            sql = await db.cursor()
            await sql.execute(my_changes, values)
            await db.commit()
            await on_transaction_event()
            return

        except aiosqlite.ProgrammingError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("ProgrammingError")
            await sleep(3)

        except aiosqlite.OperationalError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("OperationalError")
            await sleep(3)

        except aiosqlite.NotSupportedError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("NotSupportedError")
            await sleep(3)


async def full_select(my_select):
    for i in range(3):
        try:
            sql = await db.cursor()
            return await sql.execute(my_select)

        except aiosqlite.ProgrammingError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("ProgrammingError")
            await sleep(3)

        except aiosqlite.OperationalError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("OperationalError")
            await sleep(3)

        except aiosqlite.NotSupportedError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("NotSupportedError")
            await sleep(3)


async def unfull_select(my_select, values):
    for i in range(3):
        try:
            sql = await db.cursor()
            found = await sql.execute(my_select, values)
            return await found.fetchall()
        except aiosqlite.ProgrammingError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("ProgrammingError")
            await sleep(3)

        except aiosqlite.OperationalError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("OperationalError")
            await sleep(3)

        except aiosqlite.NotSupportedError as error:
            print(f"При запросе в базу данных возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode}")
            print("NotSupportedError")
            await sleep(3)


async def on_transaction_event():
    """
    Ивент on_transaction_event вызывается после каждого коммита в бд
    Проверяет сколько транзакций до бекапа

    :param changes: кол-во коммитов для бекапа

    :return: None
    """
    global transaction
    if transaction == 15:
        transaction = 0
        backuper()
        print("backup")
        return
    transaction = transaction + 1
