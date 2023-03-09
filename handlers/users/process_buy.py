from aiogram import Bot, F, types
from typing import Any, Union
from aiogram.handlers import PreCheckoutQueryHandler
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, LabeledPrice

from helpers.keyboards.fabric import MenuCallback, BuyProduct
from helpers.keyboards.markups import *
from data.config import Settings
from typing import Union

from ..routers import user_router

from database.functions import get_products, select_by_id

@user_router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery, bot: Bot) -> Any:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@user_router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment!')
    book_type = message.successful_payment
    print(book_type)

@user_router.callback_query(BuyProduct.filter(F.action == 'buy'))
async def process_buy(message: Message, bot: Bot, callback_data: BuyProduct):
    selected_product = await select_by_id(callback_data.product_id)

    if callback_data.is_paper:
        price = LabeledPrice(label=f'Бумажный варинат', amount=(selected_product[8] * 100))
        await bot.send_invoice(
            message.from_user.id,
            title='Оформление заказа',
            description=f'Вы покупаете бумажный варинат книги «{selected_product[1]}», заполните форму ниже.',
            prices=[price],
            payload='buy-paper-book',
            provider_token=Settings.payment_token,
            currency='rub',
            need_name=True,
            need_email=True,
            need_phone_number=True,
            need_shipping_address=True
        )
    else:
        price = LabeledPrice(label=f'Цифровой варинат', amount=(selected_product[8] * 100))
        await bot.send_invoice(
            message.from_user.id,
            title='Оформление заказа',
            description=f'Вы покупаете цифровой варинат книги «{selected_product[1]}», после покупки вам будет отправлен файл книги.',
            prices=[price],
            payload='buy-digital-book',
            provider_token=Settings.payment_token,
            currency='rub'
        )