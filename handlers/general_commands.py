from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from misc import bot, dp, admin_ids
from certificate import Certificate, get_all_certificates, set_all_certificates
import logging
from .menu import menu_keyboard
from .states import AdminState, admin_keyboard

@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки Отмена.

    Parameters
    ----------
    message : types.Message
        Текст сообщения (Отмена)
    state : FSMContext
        Сброс состояния пользователя.
    """

    await state.finish()
    await message.answer('Выбрете действие:',
                         reply_markup=menu_keyboard)


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    """
    Обработчик кнопки старт. Определяет от кого пришло сообщение.

    Parameters
    ----------
    message : types.Message
        Текст сообщения
    """
    if message.from_certificate.id in admin_ids:
        await message.answer('Привет, что хочешь делать?',
                             reply_markup=admin_keyboard)
        await AdminState.wait_admin_action.set()
