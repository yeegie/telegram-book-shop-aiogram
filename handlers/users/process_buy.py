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

from database.functions import get_products, select_by_id, Order

@user_router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery, bot: Bot) -> Any:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@user_router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'Оплата прошла успешно, информацию о заказе Вы можете посмотреть у себя в профиле, там же и скачать книгу если она была утрачена.')

    book_id = message.successful_payment.invoice_payload.split('-')[2]
    book_type = message.successful_payment.invoice_payload.split('-')[1]
    price = message.successful_payment.total_amount / 100

    if message.successful_payment.order_info is None:
        await Order.create(user_id=message.from_user.id, username=f'@{message.from_user.username}', book_id=book_id, price=price, status='Завершен', finished=True)
    else:
        order_info = message.successful_payment.order_info
        shipping_address = order_info.shipping_address

        telephone = order_info.phone_number
        email = order_info.email
        address_line = f'г. {shipping_address.city}, {shipping_address.state}, {shipping_address.post_code}, {shipping_address.street_line1}'

        await Order.create_with_address(user_id=message.from_user.id, username=f'@{message.from_user.username}', book_id=book_id, price=price, address=address_line, telephone=telephone, email=email)

    if book_type == 'd':
        try:
            await bot.send_document(message.from_user.id, FSInputFile(f'resources/book_files/{book_id}.txt'))
        except:
            await bot.send_message(message.from_user.id, 'Произошла ошибка при отправке книги, свяжитесь с администратором!')
    else:
        await bot.send_message(message.from_user.id, 'Проверьте статус заказа в профиле!')

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
            payload=f'book-p-{selected_product[0]}',
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
            payload=f'book-d-{selected_product[0]}',
            provider_token=Settings.payment_token,
            currency='rub'
        )