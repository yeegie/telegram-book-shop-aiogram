from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from helpers.keyboards.fabric_admin import ChangeProductCallback
from helpers.states import ChangeBook

from handlers.routers import admin_router
from helpers.keyboards.markups_admin import edit_product, show_changes, select_product

from database.functions import UpdateBook, get_product_by_id

# Меню изменения
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'select'))
async def selected_product(message: Message, bot: Bot, callback_data: ChangeProductCallback):
    await bot.send_message(message.from_user.id, 'Что изменим?', reply_markup=edit_product(callback_data.book_id))


# Показать изменение
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'show'))
async def show_book(callback_query: CallbackQuery, callback_data: ChangeProductCallback, bot: Bot):
    book = await get_product_by_id(callback_data.book_id)
    await bot.send_photo(callback_query.from_user.id, photo=FSInputFile(f'resources/book_images/{callback_data.book_id}.png'), caption=f'''
<b>{book[1]}</b> [id: {book[0]}]
{book[4]}

Автор: {book[5]}
Жанр: {book[6]}
Год издания: {book[7]}
Цена: {book[8]} руб.
Бумажная книга? {book[9]}
Количество: {book[10]}
''',
                         reply_markup=select_product(callback_data.book_id))
    await bot.answer_callback_query(callback_query.id)

# ==== Выбор "Фото" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'photo'))
async def change_photo(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.photo)
    await bot.send_message(callback_query.from_user.id, 'Отправьте новое фото, или /cancel для отмены')
    await bot.answer_callback_query(callback_query.id)

# Ловим фото
@admin_router.message(ChangeBook.photo, F.photo)
async def get_photo(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    file = await bot.get_file(message.photo[2].file_id)
    try:
        await bot.download_file(file_path=file.file_path, destination=f'resources/book_images/{data["id"]}.png')
        await bot.send_message(message.from_user.id, 'Фото изменено', reply_markup=show_changes(data['id']))
    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка')
    await state.clear()


# ==== Выбор "Заголовок" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'title'))
async def change_title(callback_query: CallbackQuery, callback_data: ChangeProductCallback, bot: Bot, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.title)
    await bot.send_message(callback_query.from_user.id, 'Введите новое название')
    await bot.answer_callback_query(callback_query.id)

# Ловим заголовок
@admin_router.message(ChangeBook.title)
async def get_title(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_title(data['id'], message.text)
    await bot.send_message(message.from_user.id, 'Название обновлено', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Описание" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'description'))
async def change_description(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.description)
    await bot.send_message(callback_query.from_user.id, 'Введите новое описание')
    await bot.answer_callback_query(callback_query.id)

# Ловим описание
@admin_router.message(ChangeBook.description)
async def get_description(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_description(data['id'], message.text)
    await bot.send_message(message.from_user.id, 'Описание обновлено', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Автор" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'author'))
async def change_author(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.author)
    await bot.send_message(callback_query.from_user.id, 'Введите автора')
    await bot.answer_callback_query(callback_query.id)

# Ловим автора
@admin_router.message(ChangeBook.author)
async def get_author(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_author(data['id'], message.text)
    await bot.send_message(message.from_user.id, 'Автор обновлен', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Жанр" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'genre'))
async def change_genre(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.genre)
    await bot.send_message(callback_query.from_user.id, 'Введите жанр')
    await bot.answer_callback_query(callback_query.id)

# Ловим жанр
@admin_router.message(ChangeBook.genre)
async def get_genre(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_genre(data['id'], message.text)
    await bot.send_message(message.from_user.id, 'Жанр обновлен', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Дата выхода" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'release_date'))
async def change_release_date(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.releaseDate)
    await bot.send_message(callback_query.from_user.id, 'Введите год выхода')
    await bot.answer_callback_query(callback_query.id)

# Ловим год выхода
@admin_router.message(ChangeBook.releaseDate)
async def get_release_date(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_release_date(data['id'], message.text)
    await bot.send_message(message.from_user.id, 'Дата обновлена', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Цена" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'price'))
async def change_price(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.price)
    await bot.send_message(callback_query.from_user.id, 'Введите цену')
    await bot.answer_callback_query(callback_query.id)

# Ловим цену
@admin_router.message(ChangeBook.price)
async def get_price(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await UpdateBook.update_price(data['id'], int(message.text))
    await bot.send_message(message.from_user.id, 'Цена обновлена', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "Типа книги" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'limited'))
async def change_limited(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.limited)
    await bot.send_message(callback_query.from_user.id, 'Книга цифровая? да/нет')
    await bot.answer_callback_query(callback_query.id)

# Ловим limited
@admin_router.message(ChangeBook.limited)
async def get_limited(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    answer = None
    if str.lower(message.text) == 'да':
        answer = False
    elif str.lower(message.text) == 'нет':
        answer = True
    else:
        await bot.send_message(message.from_user.id, 'Не понял вашего ответа, напишите ещё раз, да или нет')
    await UpdateBook.update_limited(data['id'], answer)
    await bot.send_message(message.from_user.id, 'Тип обновлен', reply_markup=show_changes(data['id']))
    await state.clear()


# ==== Выбор "количество" ====
@admin_router.callback_query(ChangeProductCallback.filter(F.action == 'quantity'))
async def change_quantity(callback_query: CallbackQuery, bot: Bot, callback_data: ChangeProductCallback, state: FSMContext):
    await state.set_state(ChangeBook.id)
    await state.update_data(id=callback_data.book_id)

    await state.set_state(ChangeBook.quantity)
    await bot.send_message(callback_query.from_user.id, 'Введите количество')
    await bot.answer_callback_query(callback_query.id)

# Ловим количество
@admin_router.message(ChangeBook.quantity)
async def get_quantity(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    try:
        await UpdateBook.update_quantity(data['id'], int(message.text))
        await bot.send_message(message.from_user.id, 'Количество обновлено', reply_markup=show_changes(data['id']))
        await state.clear()
    except:
        await bot.send_message(message.from_user.id, 'Введите число')