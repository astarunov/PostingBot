from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dateutil import parser
from Keyboards import reply, inline
from aiogram.filters import CommandStart, Command, CommandObject

router = Router()
scheduler = AsyncIOScheduler()
CHANNEL_ID = -1002449356618


@router.message(CommandStart())
async def start(message: Message):
    try:
        # Получаем данные о канале
        chat = await message.bot.get_chat(CHANNEL_ID)
        channel_name = chat.title

        # Создаем ссылку на канал
        if chat.invite_link:
            channel_link = chat.invite_link
        elif chat.username:
            channel_link = f"https://t.me/{chat.username}"
        else:
            channel_link = "Ссылка недоступна"

        # Формируем текст для ответа
        response_text = (
            "Привет, это твой личный помощник в ведении твоего канала!\n"
            f"[{channel_name}]({channel_link})\n"
        )

        # Отправляем ответ пользователю
        await message.answer(response_text, reply_markup=reply.main, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"Не удалось получить информацию о канале: {e}", reply_markup=reply.main)
async def post_to_channel(bot, chat_id: int = -1002449356618, text: str = "Запланированный пост"):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в канал: {e}")

async def get_channel_name(bot, chat_id: int):
    try:
        chat = await bot.get_chat(chat_id)
        return chat.title  # Возвращает название канала
    except Exception as e:
        return f"Ошибка получения названия канала: {str(e)}"

@router.message(lambda message: message.text in ["Запланировать пост", "Запланировать новый пост"])
async def schedule_post(message: Message):
    await message.answer(
        "Пожалуйста, введи данные в формате:\n\nГГГГ-ММ-ДД ЧЧ:ММ | текст поста",
        reply_markup=inline.inline_postnow
    )

@router.callback_query(lambda callback_query: callback_query.data == "new_post")
async def inline_schedule_post(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "Пожалуйста, введи данные в формате:\n\nГГГГ-ММ-ДД ЧЧ:ММ | текст поста",
        reply_markup=inline.inline_postnow
    )
    await callback_query.answer()

@router.callback_query(lambda callback_query: callback_query.data == "post_now")
async def inline_post_now(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "Пожалуйста, введи текст поста:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback_query.answer()

@router.message()
async def process_message(message: Message):
    if "|" in message.text:
        post_time_str, post_text = message.text.split('|', 1)
        post_time_str = post_time_str.strip()
        post_text = post_text.strip()

        try:
            post_time = parser.parse(post_time_str, fuzzy=False)
            chat_name = await get_channel_name(message.bot, -1002449356618)
            scheduler.add_job(post_to_channel, 'date', run_date=post_time, args=[message.bot, -1002449356618, post_text])
            await message.answer(f"Пост будет опубликован в {post_time} в канале {chat_name}", reply_markup=inline.inline_main)
        except ValueError:
            await message.answer(
                "Ошибка формата даты и времени. Убедись, что дата и время указаны в формате ГГГГ-ММ-ДД ЧЧ:ММ.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {str(e)}")
    elif message.reply_to_message:
        if message.reply_to_message.text == "Пожалуйста, введи текст поста:":
            try:
                await post_to_channel(message.bot, -1002449356618, message.text)
                await message.answer("Пост опубликован немедленно.", reply_markup=reply.main)
            except Exception as e:
                await message.answer(f"Произошла ошибка при публикации поста: {str(e)}")
        else:
            print(f"Получено сообщение, но не от кнопки 'Отправить сейчас': {message.reply_to_message.text}")
    else:
        print("Получено сообщение, но нет ответа на ожидаемое сообщение.")
