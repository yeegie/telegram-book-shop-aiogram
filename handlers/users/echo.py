from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..routers import user_router

@user_router.message()
async def echo(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, message.text)
