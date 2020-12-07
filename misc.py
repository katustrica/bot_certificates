import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser


config = configparser.ConfigParser()
config.read('.\\config.ini')
token = config['bot']['token']
admin_ids = [int(id) for id in config['admins'].values()]
bot = Bot(token=token)  # Ключ телеграм бота.
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
logging.basicConfig(level=logging.INFO)
