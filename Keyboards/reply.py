from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,


)



main = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text = "Запланировать пост"),
        KeyboardButton(text = "Контент-план")
    ],[
        KeyboardButton(text = "Креативы"),
        KeyboardButton(text = "Настройки")
    ]]
)