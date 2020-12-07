from misc import dp, bot
from aiogram.types import Message
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging

from .states import AdminState, CreateCertificate, cancel_keyboard, admin_keyboard
from .menu import show_search
from certificate import get_all_certificates


name = ''

@dp.message_handler(state=AdminState.wait_admin_action)
async def admin_menu(message: Message, state: FSMContext):
    """
    Действия в меню для админа.

    Parameters
    ----------
    message : Message
        Сообщение
    state : FSMContext
        Состояние админа
    """
    if message.text == 'Информация о сертификатах':
        certificates_msgs = "\n".join([c.certificate_info for c in get_all_certificates()])
        await message.answer(certificates_msgs)
    if message.text == 'Создать новый сертификат':
        await CreateCertificate.waiting_for_name.set()
        await message.answer('Введи название курса', reply_markup=cancel_keyboard)

@dp.message_handler(state=AdminState.waiting_for_name)
async def admin_send_message(message: Message, state: FSMContext):
    """
    Отправить сообщение всем пользователям.

    Parameters
    ----------
    message : Message
        Сообщение
    state : FSMContext
        Состояние админа
    """
    if message.text == 'Отмена':
        await AdminState.wait_admin_action.set()
        await message.answer('Выбери действие',
                             reply_markup=admin_keyboard)
    else:
        certificates = get_all_certificates()
        photo = message.photo
        video = message.video
        text = message.text
        for certificate in certificates:
            if photo:
                await bot.send_photo(certificate, photo[-1].file_id)
            if video:
                await bot.send_video(certificate, video.file_id)
            if text:
                await bot.send_message(certificate, text)

