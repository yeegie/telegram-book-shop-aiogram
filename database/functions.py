import tortoise
from tortoise.expressions import Q
from .models import Book
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