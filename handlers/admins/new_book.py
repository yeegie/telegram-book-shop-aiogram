from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from helpers.keyboards.fabric_admin import ChangeProductCallback
from helpers.states import NewBook

from handlers.routers import admin_router
from helpers.keyboards.markups_admin import edit_product, show_changes, select_product

from database.functions import CreateBook

@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'delete_this_message'), Command(commands='cancel'))
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.clear()

@admin_router.message(NewBook.title)
async def get_title(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(title=message.text)
    await bot.send_message(message.from_user.id, 'Введите описание')
    await state.set_state(NewBook.description)

@admin_router.message(NewBook.description)
async def get_description(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(description=message.text)
    await bot.send_message(message.from_user.id, 'Введите автора')
    await state.set_state(NewBook.author)

@admin_router.message(NewBook.author)
async def get_author(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(author=message.text)
    await bot.send_message(message.from_user.id, 'Введите жанр')
    await state.set_state(NewBook.genre)

@admin_router.message(NewBook.genre)
async def get_genre(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(genre=message.text)
    await bot.send_message(message.from_user.id, 'Введите год выхода')
    await state.set_state(NewBook.releaseDate)

@admin_router.message(NewBook.releaseDate)
async def get_release_date(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(release_date=message.text)
    await bot.send_message(message.from_user.id, 'Введите цену')
    await state.set_state(NewBook.price)

@admin_router.message(NewBook.price)
async def get_price(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.update_data(price=int(message.text))
    except:
        await bot.send_message(message.from_user.id, 'Введите целочисленное значение')

    await bot.send_message(message.from_user.id, 'Кинга является цифровой? да/нет')
    await state.set_state(NewBook.limited)

@admin_router.message(NewBook.limited)
async def get_limited(message: Message, bot: Bot, state: FSMContext):
    if str.lower(message.text) == 'да':
        await state.update_data(limited=False)
        await state.update_data(quantity=0)
        data = await state.get_data()
        print(data)
        await CreateBook.new(data['title'], data['description'], data['author'], data['genre'], data['release_date'], data['price'], data['limited'], data['quantity'])
    elif str.lower(message.text) == 'нет':
        await state.update_data(limited=True)
    else:
        await bot.send_message(message.from_user.id, 'Введите корректный ответ')