import yadisk
from config import settings


yandexdisk = yadisk.YaDisk(token=settings['yadisk_token'])


def backuper():
    """
    Метод backuper() отвечает за бекап БД на яндекс диск

    Ничего в себя не принимает

    :return: Null
    """
    yandexdisk.upload(settings['db_path'], '/ShopDB', overwrite=True)
