from aiogram.fsm.state import State, StatesGroup


class ChangeBook(StatesGroup):
    id = State()
    photo = State()
    file = State()
    title = State()
    description = State()
    author = State()
    genre = State()
    releaseDate = State()
    price = State()
    limited = State()
    quantity = State()