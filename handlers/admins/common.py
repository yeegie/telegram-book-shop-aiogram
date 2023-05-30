import bot
from aiogram import F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import Message, CallbackQuery, FSInputFile

from helpers.keyboards.fabric import CommonActionsCallback
from helpers.keyboards.fabric_admin import ChangeProductCallback

from aiogram.filters import Command

from ..routers import admin_router

from database.functions import Users

@admin_router.message(Command(commands='improve'))
async def login(message: Message, state: FSMContext, bot: Bot, command: CommandObject):

    try:
        user_id = int(message.text.split(' ')[1])
        role = str.lower(message.text.split(' ')[2])
    except:
        await bot.send_message(message.from_user.id, 'Пример\n/improve 423220323 admin')

    await Users.change_role_by_id(user_id, role)
