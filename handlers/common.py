from aiogram import F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import Message, CallbackQuery, FSInputFile

from helpers.keyboards.fabric import CommonActionsCallback
from helpers.keyboards.fabric_admin import ChangeProductCallback

from aiogram.filters import Command

from .routers import admin_router
from .routers import user_router

@user_router.message(Command(commands='login'))
async def login(message: Message, state: FSMContext):
    print('LOGIN')