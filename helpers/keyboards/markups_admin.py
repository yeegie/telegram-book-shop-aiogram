import locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton
from database.models import Book, User

from .fabric_admin import AdminMenuCallBack, ChangeProductCallback

btn_back = InlineKeyboardButton(text='Назад', callback_data=AdminMenuCallBack(action='back').pack())

def menu():
    markup = InlineKeyboardBuilder()

    btn_add_book = InlineKeyboardButton(text='Добавить книгу', callback_data=AdminMenuCallBack(action='add_book').pack())
    btn_edit_products = InlineKeyboardButton(text='Изменение книг', callback_data=AdminMenuCallBack(action='edit_products').pack())
    btn_stats = InlineKeyboardButton(text='Отчет', callback_data=AdminMenuCallBack(action='stats').pack())
    btn_mailing = InlineKeyboardButton(text='Рассылка', callback_data=AdminMenuCallBack(action='mailing').pack())
    btn_security = InlineKeyboardButton(text='Безопасность', callback_data=AdminMenuCallBack(action='security').pack())
    btn_settings = InlineKeyboardButton(text='Настройки', callback_data=AdminMenuCallBack(action='settings').pack())

    markup.row(btn_add_book)
    markup.row(btn_edit_products)
    markup.row(btn_stats)
    markup.row(btn_mailing)
    markup.row(btn_security)
    markup.row(btn_settings)

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
