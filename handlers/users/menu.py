from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, LabeledPrice, InputMedia

from helpers.phrases import get_random_phrases, phrases_end
from helpers.keyboards.fabric import MenuCallback, BuyProduct, FilterSettingsCallback, OrderByCallback
from helpers.keyboards.markups import menu, products, buy_product, filter_settings, genre_list, author_list, catalog
from helpers.functions import delete_and_send_photo, delete_and_send_message, edit_message
from data.config import Settings
from typing import Union

from ..routers import user_router

from database.functions import get_products, select_by_id, SortBy, get_genres


@user_router.callback_query(MenuCallback.filter(F.action == 'show_catalog'))
async def show_catalog(callback_query: CallbackQuery, bot: Bot):
    await delete_and_send_message(bot, callback_query, 'Что вам показать?', catalog())
    await bot.answer_callback_query(callback_query.id)

@user_router.callback_query(MenuCallback.filter(F.action == 'show_products'))
async def show_products(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    books_pool = await get_products()
    for book in books_pool:
        if book[9] is True:  # Если книга бумажная
            await bot.send_photo(
                callback_query.from_user.id,
                photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
<b>На складе: {book[10]} шт.</b>

Бумажный варинат
                        ''',
                reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
            )
        if book[9] is False:  # Если книга цифровая
            await bot.send_photo(
                callback_query.from_user.id,
                photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}

Цифровой варинат
            ''',
                reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
            )

    end_phrase = get_random_phrases(phrases_end)
    await bot.send_message(callback_query.from_user.id, end_phrase, reply_markup=products())
    await bot.answer_callback_query(callback_query.id)


@user_router.callback_query(MenuCallback.filter(F.action == 'back_menu'))
async def back(callback_query: CallbackQuery, bot: Bot):
    await delete_and_send_photo(bot, callback_query, FSInputFile(f'resources/menu/menu.png'), menu())

@user_router.callback_query(MenuCallback.filter(F.action == 'filter_settings'))
async def show_filter_menu(callback_query: CallbackQuery, bot: Bot):
    await edit_message(bot, callback_query, 'Выберите интересующий вас фильтр', filter_settings())

@user_router.callback_query(FilterSettingsCallback.filter())
async def show_filter_settings(callback_query: CallbackQuery, bot: Bot, callback_data: FilterSettingsCallback):
    book_pool = None

    if callback_data.category == 'genre':
        await edit_message(bot, callback_query, 'Выберите жанр', await genre_list())
    elif callback_data.category == 'author':
        await edit_message(bot, callback_query, 'Выберите автора', await author_list())
    elif callback_data.category == 'digital':
        book_pool = await SortBy.limited(0)
    elif callback_data.category == 'paper':
        book_pool = await SortBy.limited(1)
    elif callback_data.category == 'low_price':
        book_pool = await SortBy.price()
    elif callback_data.category == 'popular':
        book_pool = await SortBy.popular()

    if book_pool is None or book_pool == []:
        pass
    else:
        for book in book_pool:
            if book[9] is True:  # Если книга бумажная
                await bot.send_photo(
                    callback_query.from_user.id,
                    photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                    caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
<b>На складе: {book[10]} шт.</b>

Бумажный варинат
                                ''',
                    reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
                )
            if book[9] is False:  # Если книга цифровая
                await bot.send_photo(
                    callback_query.from_user.id,
                    photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                    caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}

Цифровой варинат
                    ''',
                    reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
                )

        end_phrase = get_random_phrases(phrases_end)
        await bot.send_message(callback_query.from_user.id, end_phrase, reply_markup=products())
        await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query.id)

@user_router.callback_query(OrderByCallback.filter(F.type))
async def selected_genre(callback_query: CallbackQuery, callback_data: OrderByCallback, bot: Bot):
    book_pool = []

    if callback_data.type == 'author':
        book_pool = await SortBy.author(callback_data.value)
    elif callback_data.type == 'genre':
        book_pool = await SortBy.genre(callback_data.value)

    if book_pool is None or book_pool == []:
        pass
    else:
        for book in book_pool:
            if book[9] is True:  # Если книга бумажная
                await bot.send_photo(
                    callback_query.from_user.id,
                    photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                    caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
<b>На складе: {book[10]} шт.</b>

Бумажный варинат
                                            ''',
                    reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
                )
            if book[9] is False:  # Если книга цифровая
                await bot.send_photo(
                    callback_query.from_user.id,
                    photo=FSInputFile(f'resources/book_images/{book[0]}.png'),
                    caption=f'''
<b>{book[1]}</b>
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}

Цифровой варинат
                    ''',
                    reply_markup=buy_product(price=book[8], id=book[0], is_paper=book[9])
                )

        end_phrase = get_random_phrases(phrases_end)
        await bot.send_message(callback_query.from_user.id, end_phrase, reply_markup=products())
        await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query.id)
