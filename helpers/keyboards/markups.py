import locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from database.models import Book
from .fabric import MenuCallback

def menu():
    markup = InlineKeyboardBuilder()

    btn_show_products = InlineKeyboardButton(text='Каталог 📚', callback_data=MenuCallback(action='show_products').pack())
    btn_show_profile = InlineKeyboardButton(text='Профиль 👤', callback_data=MenuCallback(action='show_products').pack())

    markup.add(btn_show_products)
    markup.add(btn_show_profile)

    return markup.as_markup(resize_keyboard=True)

def products():
    markup = InlineKeyboardBuilder()

    btn_settings = InlineKeyboardButton(text='Фильтр', callback_data=MenuCallback(action='filter_settings').pack())
    btn_main_menu = InlineKeyboardButton(text='Назад', callback_data=MenuCallback(action='back_menu').pack())

    markup.add(btn_settings)
    markup.add(btn_main_menu)

    return markup.as_markup(resize_keyboard=True)

