from aiogram.utils.keyboard import CallbackData

class AdminMenuCallBack(CallbackData, prefix='admin-menu'):
    action: str

class ChangeProductCallback(CallbackData, prefix='product'):
    action: str
    book_id: int