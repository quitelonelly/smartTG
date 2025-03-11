from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Основная клавиатура
kb_con = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поделиться контактом', request_contact=True)]
    ],
    resize_keyboard=True
)
    
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, хочу аудит", callback_data="want_audit"),
            InlineKeyboardButton(text="❌ Нет, позже", callback_data="later")
        ]
    ]
)