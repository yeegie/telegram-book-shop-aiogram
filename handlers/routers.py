from aiogram import Router, F
from filters.admin_filter import IsAdmin

user_router = Router()
admin_router = Router()

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())
