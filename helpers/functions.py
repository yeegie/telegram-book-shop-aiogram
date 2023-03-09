from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

async def delete_and_send_photo(bot: Bot, callback_query: CallbackQuery, photo: FSInputFile, markup=None):
    '''
    Сначала происходит удаление сообщение, потом отправка нового.
    '''
    await callback_query.message.delete()
    if markup is None:
        await bot.send_photo(callback_query.from_user.id, photo)
    else:
        await bot.send_photo(callback_query.from_user.id, photo, reply_markup=markup)
    await bot.answer_callback_query(callback_query.id)

async def delete_and_send_message(bot: Bot, callback_query: CallbackQuery, text: str, markup=None):
    await callback_query.message.delete()
    if markup is None:
        await bot.send_message(callback_query.from_user.id, text)
    else:
        await bot.send_message(callback_query.from_user.id, text, reply_markup=markup)
    await bot.answer_callback_query(callback_query.id)

async def edit_message(bot: Bot, callback_query: CallbackQuery, text: str, markup=None):
    if markup is None:
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id)
    else:
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=markup)
    await bot.answer_callback_query(callback_query.id)