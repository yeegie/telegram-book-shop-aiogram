import locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton
from database.models import Book, User

from .fabric_admin import AdminMenuCallBack, ChangeProductCallback, ChangeOrderCallback, ChangeOrderStatusCallback

btn_back = InlineKeyboardButton(text='Назад', callback_data=AdminMenuCallBack(action='back').pack())

def menu():
    markup = InlineKeyboardBuilder()

    btn_add_book = InlineKeyboardButton(text='Добавить книгу', callback_data=AdminMenuCallBack(action='add_book').pack())
    btn_edit_products = InlineKeyboardButton(text='Изменить книгу', callback_data=AdminMenuCallBack(action='edit_products').pack())
    btn_delete_product = InlineKeyboardButton(text='Удалить книгу', callback_data=AdminMenuCallBack(action='delete_product').pack())
    btn_orders = InlineKeyboardButton(text='Заказы', callback_data=AdminMenuCallBack(action='orders').pack())
    btn_stats = InlineKeyboardButton(text='Отчет', callback_data=AdminMenuCallBack(action='stats').pack())
    btn_mailing = InlineKeyboardButton(text='Рассылка', callback_data=AdminMenuCallBack(action='mailing').pack())
    btn_security = InlineKeyboardButton(text='Безопасность', callback_data=AdminMenuCallBack(action='security').pack())
    btn_settings = InlineKeyboardButton(text='Настройки', callback_data=AdminMenuCallBack(action='settings').pack())

    markup.row(btn_add_book, btn_edit_products)
    markup.row(btn_delete_product)
    markup.row(btn_orders)
    markup.row(btn_stats)
    markup.row(btn_mailing)
    # markup.row(btn_security)
    # markup.row(btn_settings)

    return markup.as_markup()

def select_product(book_id: int):
    markup = InlineKeyboardBuilder()

    btn_change = InlineKeyboardButton(text='Изменить', callback_data=ChangeProductCallback(action='select', book_id=book_id).pack())

    markup.add(btn_change)

    return markup.as_markup()

def edit_product(book_id):
    markup = InlineKeyboardBuilder()

    btn_photo = InlineKeyboardButton(text='Фото 🖼', callback_data=ChangeProductCallback(action='photo', book_id=book_id).pack())
    btn_file = InlineKeyboardButton(text='Файл 📄', callback_data=ChangeProductCallback(action='file', book_id=book_id).pack())
    btn_title = InlineKeyboardButton(text='Заголовок ✏', callback_data=ChangeProductCallback(action='title', book_id=book_id).pack())
    btn_description = InlineKeyboardButton(text='Описание 📕', callback_data=ChangeProductCallback(action='description', book_id=book_id).pack())
    btn_author = InlineKeyboardButton(text='Автор 👤', callback_data=ChangeProductCallback(action='author', book_id=book_id).pack())
    btn_genre = InlineKeyboardButton(text='Жанр 🤔', callback_data=ChangeProductCallback(action='genre', book_id=book_id).pack())
    btn_release_date = InlineKeyboardButton(text='Дата выхода 📅', callback_data=ChangeProductCallback(action='release_date', book_id=book_id).pack())
    btn_price = InlineKeyboardButton(text='Цену 💰', callback_data=ChangeProductCallback(action='price', book_id=book_id).pack())
    btn_limited = InlineKeyboardButton(text='Варинат', callback_data=ChangeProductCallback(action='limited', book_id=book_id).pack())
    btn_quantity = InlineKeyboardButton(text='Количество', callback_data=ChangeProductCallback(action='quantity', book_id=book_id).pack())
    btn_cancel_action = InlineKeyboardButton(text='Отмена', callback_data=ChangeProductCallback(action='delete_this_message', book_id=book_id).pack())

    markup.row(btn_photo, btn_file)
    markup.row(btn_title, btn_description)
    markup.row(btn_author, btn_genre)
    markup.row(btn_release_date)
    markup.row(btn_price)
    markup.row(btn_limited, btn_quantity)
    markup.row(btn_cancel_action)

    return markup.as_markup()

def show_changes(book_id):
    markup = InlineKeyboardBuilder()

    btn_show = InlineKeyboardButton(text='Показать', callback_data=ChangeProductCallback(action='show', book_id=book_id).pack())

    markup.row(btn_show)

    return markup.as_markup()

def show_orders_menu():
    markup = InlineKeyboardBuilder()

    btn_archive = InlineKeyboardButton(text='Архив заказов', callback_data=AdminMenuCallBack(action='orders_archive').pack())
    btn_active_orders = InlineKeyboardButton(text='Активные заказы', callback_data=AdminMenuCallBack(action='orders_active').pack())

    markup.row(btn_archive)
    markup.row(btn_active_orders)
    markup.row(btn_back)

    return markup.as_markup()

def edit_order(order_id):
    markup = InlineKeyboardBuilder()

    btn_edit = InlineKeyboardButton(text='Изменить', callback_data=ChangeOrderCallback(action='edit_order', order_id=order_id).pack())

    markup.row(btn_edit)

    return markup.as_markup()

def edit_order_info(order_id):
    markup = InlineKeyboardBuilder()

    btn_status = InlineKeyboardButton(text='Статус заказа', callback_data=ChangeOrderCallback(action='status', order_id=order_id).pack())

    markup.row(btn_status)

    return markup.as_markup()

def status_variants(order_id):
    markup = InlineKeyboardBuilder()

    btn_send = InlineKeyboardButton(text='Отправлен', callback_data=ChangeOrderStatusCallback(status='sended', order_id=order_id).pack())
    btn_waiting = InlineKeyboardButton(text='Ожидает получения', callback_data=ChangeOrderStatusCallback(status='waited', order_id=order_id).pack())
    btn_finished = InlineKeyboardButton(text='Завершен', callback_data=ChangeOrderStatusCallback(status='finished', order_id=order_id).pack())

    markup.row(btn_send)
    markup.row(btn_waiting)
    markup.row(btn_finished)

    return markup.as_markup()