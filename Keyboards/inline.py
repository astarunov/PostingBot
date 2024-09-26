from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Запланировать новый пост", callback_data="new_post")
    ]]
)

postnow = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Опубликовать сейчас", callback_data="post_now")]])

postchange = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Удалить описание", callback_data="remove_caption")],[
        InlineKeyboardButton(text="Изменить описание", callback_data="edit_caption")],[
        InlineKeyboardButton(text="Добавить конпку", callback_data="add_button")],[
        InlineKeyboardButton(text="<-Отменить", callback_data="cancel"),
        InlineKeyboardButton(text="Далее->", callback_data="next_step")]

    ])