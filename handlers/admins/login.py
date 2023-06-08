from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from ..routers import admin_router, user_router

from helpers.states import Login

from data.config import Settings

from database.functions import Users

from datetime import datetime


@user_router.message(Command(commands='login'))
async def admin_authorization(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, 'Введите пароль')
    await state.clear()
    await state.set_state(Login.password)

@user_router.message(Login.password)
async def get_password(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    if (data['password'] == Settings.password) and (await Users.get_user_role(message.from_user.id) == 'user'):
        await message.answer('Вы повышены до администратора')
        await Users.change_role_by_id(message.from_user.id, 'admin')
        print(f'[!] @{message.from_user.username} повышен до администратора! {datetime.now()}')
    else:
        await message.answer('Ошибка!')
    await state.clear()
