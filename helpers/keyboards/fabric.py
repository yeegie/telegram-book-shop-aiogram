from aiogram.utils.keyboard import CallbackData

class MenuCallback(CallbackData, prefix='menu'):
    action: str

class SelectedGenre(CallbackData, prefix='genre'):
    genre: str

class BuyProduct(CallbackData, prefix='product'):
    action: str
    product_id: int
    is_paper: bool

class CommonActionsCallback(CallbackData, prefix='common'):
    action: str

class FilterSettingsCallback(CallbackData, prefix='filter'):
    category: str

class OrderByCallback(CallbackData, prefix='order'):
    type: str
    value: str
