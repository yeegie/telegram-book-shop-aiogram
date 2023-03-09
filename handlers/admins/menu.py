from aiogram import F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from helpers.keyboards.markups_admin import menu, select_product, edit_product
from helpers.keyboards.fabric_admin import AdminMenuCallBack, ChangeProductCallback

from database.functions import get_products

from ..routers import admin_router


@admin_router.message(Command(commands='admin'))
async def admin_panel(callback_query: CallbackQuery, bot: Bot):
    await bot.send_photo(callback_query.from_user.id, photo=FSInputFile(f'resources/menu/menu.png'), reply_markup=menu())

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'edit_products'))
async def select_products(callback_query: CallbackQuery, bot: Bot):
    books_pool = await get_products()
    for book in books_pool:
        if book[9] is True:  # Если книга бумажная
            await bot.send_photo(
                callback_query.from_user.id,
                photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                caption=f'''
<b>{book[1]}</b> [id: {book[0]}]
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
<b>На складе: {book[10]} шт.</b>

Бумажный варинат
                            ''',
                reply_markup=select_product(book[0])
            )
        if book[9] is False:  # Если книга цифровая
            await bot.send_photo(
                callback_query.from_user.id,
                photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                caption=f'''
<b>{book[1]}</b> [id: {book[0]}]
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}

Цифровой варинат
                ''',
                reply_markup=select_product(book[0])
            )
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'stats'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('stats')
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'mailing'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('mailing')
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'security'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('security')
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'settings'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('settings')
    await bot.answer_callback_query(callback_query.id)