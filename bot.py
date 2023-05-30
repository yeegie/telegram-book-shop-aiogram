import database

from data.config import Telegram, Webhooks

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application, run_app

from handlers.routers import user_router, admin_router

from middlewares.base_middleware import MyMiddleware

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
    bot = Bot(token=Telegram.token, parse_mode='HTML')
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    dispatcher.startup.register(on_startup)

    application = Application()

    application['bot'] = bot
    application['dp'] = dispatcher

    SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(application, Webhooks.bot_path)

    setup_application(application, dispatcher, bot=bot)
    run_app(application, host=Webhooks.listen_address, port=Webhooks.listen_port)


