import tortoise
from tortoise.expressions import Q
from .models import Book, User, Sales
import numpy as np


async def get_genres():
    return np.unique(await Book.all().values_list('genre'))

async def get_authors():
    return np.unique(await Book.all().values_list('author'))

async def get_products():
    books_pool = await Book.all().values_list()
    return books_pool

async def get_product_by_id(product_id: int):
    product = await Book.get(id=product_id).values_list()
    return product

async def select_by_id(product_id: int):
    return await Book.get(id=product_id).values_list()

class SortBy:
    @staticmethod
    async def limited(value: int):
        '''
        :param: 0 is digital book, 1 is paper book
        :return: book list
        '''
        books = await Book.filter(limited=value).values_list()
        return books

    @staticmethod
    async def price():
        books = await Book.all().order_by('price').values_list()
        return books

    @staticmethod
    async def popular():
        books = await Book.all().order_by('likes').values_list()
        return books

    @staticmethod
    async def genre(value):
        books = await Book.filter(genre=value).values_list()
        return books

    @staticmethod
    async def author(value):
        books = await Book.filter(author=value).values_list()
        return books

class UpdateBook:
    @staticmethod
    async def update_title(book_id: int, new_title: str):
        book = await Book.get_or_none(id=book_id)
        book.title = new_title
        await book.save()

    @staticmethod
    async def update_description(book_id: int, new_description: str):
        book = await Book.get_or_none(id=book_id)
        book.description = new_description
        await book.save()

    @staticmethod
    async def update_author(book_id: int, new_author: str):
        book = await Book.get_or_none(id=book_id)
        book.author = new_author
        await book.save()

    @staticmethod
    async def update_genre(book_id: int, new_genre: str):
        book = await Book.get_or_none(id=book_id)
        book.genre = new_genre
        await book.save()

    @staticmethod
    async def update_release_date(book_id: int, new_date: str):
        book = await Book.get_or_none(id=book_id)
        book.releaseDate = new_date
        await book.save()

    @staticmethod
    async def update_price(book_id: int, new_price: int):
        book = await Book.get_or_none(id=book_id)
        book.price = new_price
        await book.save()

    @staticmethod
    async def update_limited(book_id: int, new_type: bool):
        book = await Book.get_or_none(id=book_id)
        book.limited = new_type
        await book.save()

    @staticmethod
    async def update_quantity(book_id: int, new_quantity: int):
        book = await Book.get_or_none(id=book_id)
        book.quantity = new_quantity
        await book.save()

class CreateBook:
    @staticmethod
    async def new(title, description, author, genre, release_date, price, limited, quantity):
        await Book.create(title=title, description=description, author=author, genre=genre,
                          releaseDate=release_date, price=price, limited=limited, quantity=quantity)

class Users:
    @staticmethod
    async def change_role_by_id(user_id: int, role: str):
        await User.get_or_create(user_id=user_id, type=role)

class Order:
    @staticmethod
    async def get(order_id: int):
        '''Получить заказ по id'''
        return await Sales.get(id=order_id).values_list()

    @staticmethod
    async def create_with_address(user_id: int, username: str, book_id: int, price: int, address: str, telephone: str, email: str):
        '''Создать чек с адресом'''
        await Sales.create(user_id=user_id, username=username, book_id=book_id, price=price, address=address, telephone=telephone, email=email)

    @staticmethod
    async def create(user_id: int, username: str, book_id: int, price: int, status=None, finished=None):
        '''Создать чек без адреса'''
        await Sales.create(user_id=user_id, username=username, book_id=book_id, price=price, status=status, finished=finished)

    @staticmethod
    async def active():
        '''Все не законченные заказы'''
        orders_pool = await Sales.filter(finished=False).values_list()
        return orders_pool

    @staticmethod
    async def all_orders():
        '''Вывести все заказы'''
        orders_pool = await Sales.all().values_list()
        return orders_pool

    @staticmethod
    async def update_status(order_id: int, status: str, finished=False):
        order = await Sales.filter(id=order_id).first()
        order.status = status
        order.finished = finished
        await order.save()


