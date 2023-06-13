import asyncio

import database

from data.config import Telegram, Webhooks

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram.client.session.aiohttp import AiohttpSession

from handlers.routers import user_router, admin_router

from middlewares.base_middleware import MyMiddleware

from webhooks import web_application


# Webhook method
async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await database.load_database()
    print('database loaded')
    dispatcher.message.outer_middleware(MyMiddleware())
    dispatcher.callback_query.outer_middleware(MyMiddleware())
    print('middleware loaded')
    dispatcher.include_router(user_router)
    dispatcher.include_router(admin_router)
    print('routers included')

    await bot.set_webhook(f"{Webhooks.base_url}{Webhooks.bot_path}")
    print('[!] Bot started!')

if __name__ == '__main__':
    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": "HTML"}
    bot = Bot(token=Telegram.token, **bot_settings)
    storage = MemoryStorage()

    dispatcher = Dispatcher(storage=storage)
    dispatcher.startup.register(on_startup)

    web_application['bot'] = bot
    web_application['dp'] = dispatcher

    SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(web_application, path=Webhooks.bot_path)

    setup_application(web_application, dispatcher, bot=bot)
    web.run_app(web_application, host=Webhooks.listen_address, port=Webhooks.listen_port)


# Long polling method
# async def on_startup(dispatcher: Dispatcher, bot: Bot):
#     await database.load_database()
#     print('database loaded')
#     dispatcher.message.outer_middleware(MyMiddleware())
#     dispatcher.callback_query.outer_middleware(MyMiddleware())
#     print('middleware loaded')
#     dispatcher.include_router(user_router)
#     dispatcher.include_router(admin_router)
#     print('routers included')
#     print('[!] Bot started!')
#
#     await start_bot(dispatcher, bot)
#
# async def start_bot(dispatcher: Dispatcher, bot: Bot):
#     await delete_webhook(bot)
#     await dispatcher.start_polling(bot)
#
# async def delete_webhook(bot: Bot):
#     await bot.delete_webhook()
#
# if __name__ == '__main__':
#     bot = Bot(token=Telegram.token, parse_mode='HTML')
#     storage = MemoryStorage()
#     dispatcher = Dispatcher(bot=bot, storage=storage)
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(on_startup(dispatcher, bot))