from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from Keyboards import reply

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, это твой личный помощник в ведении твоего канала!", reply_markup=reply.main)
