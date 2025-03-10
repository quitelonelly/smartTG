from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Основная клавиатура
kb_con = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поделиться контактом', request_contact=True)]
    ],
    resize_keyboard=True
)
    