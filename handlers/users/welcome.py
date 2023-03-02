from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from helpers.keyboards.markups import menu
from data.config import Settings
from typing import Union

from ..routers import user_router


@user_router.message(Command(commands=['start', 'help']))
async def welcome(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer('🤖')
    await message.answer(f'''
Привет {message.from_user.first_name}!
Посмотрите наш каталог книг, просто нажмите /menu приятного чтения!
    ''')

@user_router.message(Command(commands='menu'))
async def show_menu(message: Message, bot: Bot):
    await bot.send_photo(message.from_user.id, photo=FSInputFile('resources/menu/menu.png'), reply_markup=menu())
