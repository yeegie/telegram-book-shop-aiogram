import locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from database.models import Book
from .fabric import MenuCallback, BuyProduct, FilterSettingsCallback, OrderByCallback
from database.functions import get_genres, get_authors

btn_main_menu = InlineKeyboardButton(text='Главное меню', callback_data=MenuCallback(action='back_menu').pack())
btn_filter = InlineKeyboardButton(text='К фильтрам', callback_data=MenuCallback(action='filter_settings').pack())

def menu():
    markup = InlineKeyboardBuilder()

    btn_show_products = InlineKeyboardButton(text='Каталог 📚', callback_data=MenuCallback(action='show_catalog').pack())
    btn_show_profile = InlineKeyboardButton(text='Профиль 👤', callback_data=MenuCallback(action='show_profile').pack())
    btn_settings = InlineKeyboardButton(text='Настройки ⚙', callback_data=MenuCallback(action='show_settings').pack())

    markup.add(btn_show_products)
    markup.add(btn_show_profile)
    markup.row(btn_settings)

    return markup.as_markup(resize_keyboard=True)

def catalog():
    markup = InlineKeyboardBuilder()

    btn_show_products = InlineKeyboardButton(text='Показать все книги', callback_data=MenuCallback(action='show_products').pack())
    btn_show_filter = InlineKeyboardButton(text='По категориям', callback_data=MenuCallback(action='filter_settings').pack())

    markup.row(btn_show_products)
    markup.row(btn_show_filter)

    return markup.as_markup()

def products():
    markup = InlineKeyboardBuilder()

    btn_settings = InlineKeyboardButton(text='Фильтр', callback_data=MenuCallback(action='filter_settings').pack())
    btn_main_menu = InlineKeyboardButton(text='Назад', callback_data=MenuCallback(action='back_menu').pack())

    markup.add(btn_settings)
    markup.add(btn_main_menu)

    return markup.as_markup(resize_keyboard=True)

def buy_product(price, id, is_paper):
    markup = InlineKeyboardBuilder()

    btn_buy = InlineKeyboardButton(text=f'Купить {price} ₽',
                                   callback_data=BuyProduct(action='buy',
                                                            product_id=id,
                                                            is_paper=is_paper
                                                            ).pack())

    markup.add(btn_buy)

    return markup.as_markup(resize_keyboard=True)

def filter_settings():
    markup = InlineKeyboardBuilder()

    btn_genre = InlineKeyboardButton(text='Жанр 🎭', callback_data=FilterSettingsCallback(category='genre').pack())
    btn_author = InlineKeyboardButton(text='Автор 👤', callback_data=FilterSettingsCallback(category='author').pack())
    btn_digital_books = InlineKeyboardButton(text='Цифровые книги 📱', callback_data=FilterSettingsCallback(category='digital').pack())
    btn_paper_books = InlineKeyboardButton(text='Бумажные книги 📕', callback_data=FilterSettingsCallback(category='paper').pack())
    btn_price = InlineKeyboardButton(text='Дешёвые 💸', callback_data=FilterSettingsCallback(category='low_price').pack())
    btn_popular = InlineKeyboardButton(text='Популярные ⭐', callback_data=FilterSettingsCallback(category='popular').pack())

    markup.row(btn_genre)
    markup.row(btn_author)
    markup.row(btn_digital_books)
    markup.row(btn_paper_books)
    markup.row(btn_price)
    markup.row(btn_popular)
    markup.row(btn_main_menu)

    return markup.as_markup()

async def genre_list():
    markup = InlineKeyboardBuilder()

    genres = await get_genres()
    for genre in genres:
        markup.row(InlineKeyboardButton(text=genre, callback_data=OrderByCallback(type='genre', value=genre).pack()))
    markup.row(btn_filter)
    return markup.as_markup()

async def author_list():
    markup = InlineKeyboardBuilder()

    authors = await get_authors()
    for author in authors:
        markup.row(InlineKeyboardButton(text=author, callback_data=OrderByCallback(type='author', value=author).pack()))
    markup.row(btn_filter)
    return markup.as_markup()

