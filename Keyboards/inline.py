from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

inline_main = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Запланировать новый пост", callback_data="new_post")
    ]]
)

inline_postnow = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Опубликовать сейчас", callback_data="post_now")]])