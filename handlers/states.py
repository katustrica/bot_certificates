from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup


class AdminState(StatesGroup):
    wait_admin_action = State()
    wait_message_text = State()


class CreateCertificate(StatesGroup):
    waiting_for_name = State()


admin_keyboard = ReplyKeyboardMarkup(
    [['Посмотреть все'], ['Создать новый'], ['Деактивировать']], resize_keyboard=True
)
cancel_keyboard = ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)