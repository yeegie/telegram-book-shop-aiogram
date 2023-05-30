from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from helpers.keyboards.fabric_admin import AdminMenuCallBack, ChangeOrderCallback, ChangeOrderStatusCallback

from helpers.keyboards.markups_admin import edit_order, status_variants, edit_order_info

from handlers.routers import admin_router

from database.functions import Order


@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'orders_archive'))
async def show_orders_archive(callback_query: CallbackQuery, bot: Bot):
    orders = await Order.all_orders()
    for order in orders:
        await bot.send_message(callback_query.from_user.id, f'''
<b>ID:</b> {order[0]}
user_id: {order[1]}
username: {order[3]}
book_id: {order[4]}
price: {order[5]} ₽
address: {order[6]}
telephone: {order[7]}
email: {order[8]}
date: {order[-2]}
status: {order[-1]}
''', reply_markup=edit_order(order[0]))


@admin_router.callback_query(AdminMenuCallBack.filter(F.action == 'orders_active'))
async def show_orders_active(callback_query: CallbackQuery, bot: Bot):
    orders = await Order.active()
    for order in orders:
        await bot.send_message(callback_query.from_user.id, f'''
<b>ID:</b> {order[0]}
user_id: {order[1]}
username: {order[3]}
book_id: {order[4]}
price: {order[5]} ₽
address: {order[6]}
telephone: {order[7]}
email: {order[8]}
date: {order[-2]}
status: {order[-1]}
        ''', reply_markup=edit_order(order[0]))


@admin_router.callback_query(ChangeOrderCallback.filter(F.action == 'edit_order'))
async def show_status_menu_order(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeOrderCallback):
    await bot.send_message(callback_query.from_user.id, 'хуй', reply_markup=edit_order_info(callback_data.order_id))


@admin_router.callback_query(ChangeOrderStatusCallback.filter())
async def edit_order_status(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeOrderStatusCallback):
    status = callback_data.status
    if status == 'sended':
        print('sended')
    elif status == 'waited':
        print('waited')
    elif status == 'finished':
        print('finished')

    await bot.answer_callback_query(callback_query.id)
