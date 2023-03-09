from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from typing import Union, Any, Dict, Callable, Awaitable

from database.models.user import User

from helpers.keyboards.fabric_admin import ChangeProductCallback

class MyMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Before
        user = await User.get_or_none(user_id=event.from_user.id)
        if user is None:
            user = await User.create(
                user_id=event.from_user.id,
                username=event.from_user.username
            )
        data['user'] = user
        return await handler(event, data)
