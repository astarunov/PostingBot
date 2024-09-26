from aiogram import Router, types
from Keyboards import reply, inline
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from Data import database
import os
from datetime import datetime

os.makedirs('pics', exist_ok=True)
router = Router()
CHANNEL_ID = -1002449356618

class PostState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_date = State()
    waiting_for_change = State()
    waiting_for_description = State()

@router.message(CommandStart())
async def start(message: Message):
    try:
        await database.table_create()
        chat = await message.bot.get_chat(CHANNEL_ID)
        channel_name = chat.title
        channel_link = chat.invite_link or f"https://t.me/{chat.username}" or "Ссылка недоступна"

        response_text = (
            "Привет, это твой личный помощник в ведении твоего канала!\n"
            f"[{channel_name}]({channel_link})\n"
        )
        await message.answer(response_text, reply_markup=reply.main, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Не удалось получить информацию о канале: {e}", reply_markup=reply.main)

@router.message(lambda message: message.text in ["Запланировать пост", "Запланировать новый пост"])
async def schedule_post(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте пост одним сообщением.")
    await state.set_state(PostState.waiting_for_photo)

@router.callback_query(lambda c: c.data == "new_post")
async def remove_caption_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте пост одним сообщением.")
    await state.set_state(PostState.waiting_for_photo)

@router.message(PostState.waiting_for_photo)
async def process_post(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]  # Берем самое высокое качество
        photo_id = photo.file_id
        file = await message.bot.get_file(photo_id)
        file_path = file.file_path
        file_name = f"Data/pics/{photo_id}.jpg"

        await message.bot.download_file(file_path, file_name)

        caption = message.caption or message.text
        admin_id = str(message.from_user.id)
        post_id = await database.schedule_post_f(admin_id, photo_id, caption)

        await state.update_data(post_id=post_id, photo_id=photo_id, caption=caption, admin_id=admin_id)
        await message.answer_photo(photo=photo_id, caption=caption, reply_markup=inline.postchange)
    else:
        await message.answer("Пожалуйста, отправь изображение с текстом.")

@router.callback_query(lambda c: c.data == "next_step")
async def ask_date(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Обязательно отвечаем на колбек
    await callback_query.message.answer("Введите дату публикации поста в формате:\n\nYYYY-MM-DD HH:MM:SS")
    data = await state.get_data()
    admin_id = data.get('admin_id')
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    post_id = data.get('post_id')

    await state.set_state(PostState.waiting_for_date)

@router.message(PostState.waiting_for_date)
async def process_caption_date(message: Message, state: FSMContext):
    date_input = message.text
    data = await state.get_data()
    admin_id = data.get('admin_id')
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    post_id = data.get('post_id')

    try:
        # Проверка формата даты
        post_date = datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')
        await database.schedule_post_s(post_id, post_date)

        await message.answer(f"Пост будет опубликован {date_input}")
    except ValueError:
        await message.answer("Некорректный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM:SS.")

@router.callback_query(lambda c: c.data == "remove_caption")
async def remove_caption_callback(callback_query: CallbackQuery):
    await callback_query.answer("Вы вышли из режима редактирования.")
    await callback_query.message.delete()

@router.callback_query(lambda c: c.data == "edit_caption")
async def change_post_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer("Напишите новое описание для поста.")
    data = await state.get_data()
    admin_id = data.get('admin_id')
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    post_id = data.get('post_id')
    await state.set_state(PostState.waiting_for_description)

@router.message(PostState.waiting_for_description)
async def process_new_description(message: Message, state: FSMContext):
    new_description = message.text
    admin_id = str(message.from_user.id)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    post_id = data.get('post_id')

    await database.change_text(admin_id, post_id, new_description)

    await message.answer_photo(photo=photo_id, caption=new_description, reply_markup=inline.postchange)
    await state.clear()

@router.callback_query(lambda c: c.data == "cancel")
async def exit_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Вы вышли из режима редактирования.",reply_markup=inline.main)
    data = await state.get_data()
    post_id = data.get('post_id')
    await database.cancel_drop(post_id)
    await callback_query.message.delete()

@router.message(Command("next_action"))
async def next_action(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    admin_id = data.get('admin_id')

    await message.answer(f"Admin ID: {admin_id}, Photo ID: {photo_id}, Caption: {caption}")
    await message.answer_photo(photo=f"Data/pics/{photo_id}.jpg", caption=caption)
