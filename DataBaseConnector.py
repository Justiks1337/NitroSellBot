import aiosqlite
from asyncio import sleep, run
from os import path


async def database_connect():
    while True:
        try:
            if path.exists(r"ShopDB.db"):
                print("Connect succesful")
                return await aiosqlite.connect("ShopDB.db")
            print("The database file does not exist")
            await sleep(3)

        except aiosqlite.ProgrammingError as error:
            print(f"При подключении к БД возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode} \n error traceback: {error.with_traceback()}")
            await sleep(3)

        except aiosqlite.OperationalError as error:
            print(f"При подключении к БД возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode} \n error traceback: {error.with_traceback()}")
            await sleep(3)

        except aiosqlite.NotSupportedError as error:
            print(f"При подключении к БД возникла ошибка! \n -------------------------------------------------- \n error name: {error.sqlite_errorname} \n error code: {error.sqlite_errorcode} \n error traceback: {error.with_traceback()}")
            await sleep(3)


db = run(database_connect())
