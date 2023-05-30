from aiogram.utils.keyboard import CallbackData

class AdminMenuCallBack(CallbackData, prefix='admin-menu'):
    action: str

class ChangeProductCallback(CallbackData, prefix='product'):
    action: str
    book_id: int

class ChangeOrderCallback(CallbackData, prefix='order'):
    action: str
    order_id: int

class ChangeOrderStatusCallback(CallbackData, prefix='order-status'):
    status: str
    order_id: int