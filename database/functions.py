import tortoise
from .models import Book
import numpy as np


def get_genres():
    return np.unique(Book.all().values_list('genre'))

async def get_products():
    books_pool = await Book.all().values_list()
    return books_pool
