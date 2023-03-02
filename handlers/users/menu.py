from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from helpers.keyboards.fabric import MenuCallback
from helpers.keyboards.markups import menu, products
from data.config import Settings
from typing import Union

from ..routers import user_router

from database.functions import get_products


@user_router.callback_query(MenuCallback.filter(F.action == 'show_products'))
async def show_products(message: Message, bot: Bot, state: FSMContext):
    books_pool = await get_products()
    for book in books_pool:
        await bot.send_photo(
            message.from_user.id,
            photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
            caption=f'''
<b>{book[1]}</b>
{book[4]}

Жанр: {book[6]}
Год издания: {book[7]}
<b>Цена:</b> {book[8]} ₽
''')
    await bot.send_message(message.from_user.id, 'Конец списка', reply_markup=products())