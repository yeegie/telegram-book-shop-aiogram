import matplotlib.pyplot as plt
from aiogram import F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from helpers.keyboards.markups_admin import menu, select_product, edit_product, show_orders_menu, security_menu, delete_admin
from helpers.keyboards.fabric_admin import AdminMenuCallBack, ChangeProductCallback, DeleteAdmin

from database.functions import get_products, CreateBook, Order, Users

from helpers.states import NewBook
from helpers.functions import edit_message, delete_and_send_message

from ..routers import admin_router

from datetime import datetime


@admin_router.message(Command(commands='admin'))
async def admin_panel(callback_query: CallbackQuery, bot: Bot):
    await bot.send_photo(callback_query.from_user.id, photo=FSInputFile(f'resources/menu/menu.png'), reply_markup=menu())

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'back'))
async def back_main_menu(callback_query: CallbackQuery, bot: Bot):
    await callback_query.message.delete()
    await bot.send_photo(callback_query.from_user.id, photo=FSInputFile(f'resources/menu/menu.png'), reply_markup=menu())

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'add_book'))
async def new_book(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(NewBook.title)
    await bot.send_message(callback_query.from_user.id, 'Введите название книги или нажмите /cancel для отмены')

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'edit_products'))
async def select_products(callback_query: CallbackQuery, bot: Bot):
    books_pool = await get_products()
    for book in books_pool:
        try:
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
        except:
            await bot.send_message(callback_query.from_user.id, f'''
<b>{book[1]}</b> [id: {book[0]}]
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
Цифровая {book[9]}
На складе: {book[10]} шт.
''', reply_markup=select_product(book[0]))
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'orders'))
async def show_orders(callback_query: CallbackQuery, bot: Bot):
    await delete_and_send_message(bot, callback_query, 'Панель заказов', show_orders_menu())

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'stats'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    import seaborn as sns
    import pandas as pd
    import numpy as np

    # Формируем датасет
    sales_pool = await Order.all_orders()
    df = pd.DataFrame(data=sales_pool).drop([0, 1, 2, 3, 6, 7, 8], axis=1).rename({4: 'book',
                                                                                   5: 'price',
                                                                                   9: 'date',
                                                                                   10: 'status'},
                                                                                  axis=1)

    # Текстовое сообщение
    await bot.send_message(callback_query.from_user.id, f'Общая выручка: {sum([x[5] for x in sales_pool])} ₽'
                                                        f'\nВыручка за сегодня: {sum([x[5] for x in sales_pool if x[9].day == datetime.utcnow().day])} ₽'
                                                        f'\nВыручка за месяц: {sum([x[5] for x in sales_pool if x[9].month == datetime.utcnow().month])} ₽')
    await bot.send_message(callback_query.from_user.id, '💰')



    ax = sns.scatterplot(data=df, x=df['date'].dt.month, y='price', c='red')
    # ax = sns.regplot(data=df, x=df['date'].dt.month, y='price')
    plt.grid(True)
    plt.xticks(np.arange(1, 13, step=1))
    fig = ax.get_figure()
    fig.savefig('BOB.png')

    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'mailing'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('mailing')
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'security'))
async def security_panel(callback_query: CallbackQuery, bot: Bot):
    await delete_and_send_message(bot, callback_query, 'Безопасноть 🔒', security_menu())

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'show_admins'))
async def admins_list(callback_query: CallbackQuery, bot: Bot):
    admins = await Users.get_admins()
    for admin in admins:
        await callback_query.message.answer(f'''
@{admin[-1]}
id: {admin[-2]}
type: {admin[1]}
''', reply_markup=delete_admin(admin[-2]))
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(DeleteAdmin.filter(F.action == 'delete'))
async def delete_admin_menu(callback_query: CallbackQuery, callback_data: DeleteAdmin, bot: Bot):
    await Users.change_role_by_id(callback_data.id, 'user')
    await callback_query.answer(text=f'Разжалован {callback_data.id}')
    print(f'[!] Пользователь @{callback_query.from_user.username} разжаловал {callback_data.id} {datetime.now()}')

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'change_password'))
async def change_password(callback_query: CallbackQuery, bot: Bot):
    print('cp')
    await bot.answer_callback_query(callback_query.id)

@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'settings'))
async def stats(callback_query: CallbackQuery, bot: Bot):
    print('settings')
    await bot.answer_callback_query(callback_query.id)