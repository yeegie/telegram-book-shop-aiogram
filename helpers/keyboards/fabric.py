from aiogram.utils.keyboard import CallbackData

class MenuCallback(CallbackData, prefix='menu'):
    action: str

class SelectedGenre(CallbackData, prefix='genre'):
    genre: str
