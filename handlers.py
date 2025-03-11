import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import types, Bot
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from keyboards import kb_con, inline_kb
import asyncio
from datetime import datetime  # Для работы с датой

# Настройка доступа к Google Sheets
def init_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/klim-petrov/projects/smartTG/credentials.json", scope)  # Укажите путь к вашему JSON-файлу
    client = gspread.authorize(creds)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1K6PkCuSYepOhKzk5sfm8YCxsJ8pxGBfi8IuH1VgxPIY/edit#gid=0")  # Возвращаем всю таблицу

# Начало работы бота
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! 👋\nЧтобы получить PDF-гайд «Как увеличить продажи отдела на 30% с помощью ИИ-ассистента», нажмите кнопку ниже и поделитесь вашим контактом:", parse_mode="HTML", reply_markup=kb_con)

# Отправка контакта пользователя
async def contact_handler(message: types.Message, bot: Bot):
    contact = message.contact
    sheet = init_gspread().sheet1  # Работаем с первым листом
    
    # Получаем все данные из таблицы
    records = sheet.get_all_records()
    
    # Нормализуем номер телефона (удаляем все нецифровые символы)
    def normalize_phone(phone):
        return ''.join(filter(str.isdigit, str(phone)))  # Оставляем только цифры
    
    normalized_user_phone = normalize_phone(contact.phone_number)  # Нормализуем номер пользователя
    
    # Проверяем, есть ли контакт уже в таблице
    if any(normalize_phone(record['userphone']) == normalized_user_phone for record in records):
        await message.answer("Вы уже получали гайд. Спасибо! 😊", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Спасибо! Гайд уже у вас 📩\nЗавтра вернусь и узнаю ваше мнение 😉", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

        # Отправляем PDF-файл
        pdf_file = FSInputFile("/home/klim-petrov/projects/smartTG/guide.pdf")  # Укажите путь к вашему PDF-файлу
        await message.answer_document(pdf_file)

        # Сохраняем контакт в Google Sheets (лист 1)
        # Записываем username, first_name и номер телефона
        username = message.from_user.username  # Username из Telegram
        first_name = contact.first_name  # Имя из контакта
        phone_number = contact.phone_number  # Номер телефона из контакта

        sheet.append_row([username, first_name, phone_number])  # Добавляем данные в новую строку

        # Запланировать отправку сообщения через 24 часа
        await schedule_message(bot, message.chat.id)

# Отправка сообщения после 24 часов
async def schedule_message(bot: Bot, chat_id: int):
    # Ждем 24 часа (86400 секунд)
    await asyncio.sleep(5)  # Для теста уменьшено до 5 секунд
    
    # Отправляем сообщение через 24 часа    
    await bot.send_message(
        chat_id,
        "Успели изучить гайд?\n"
        "Хотите узнать, сколько денег вы теряете прямо сейчас из-за сливов лидов? "
        "Предлагаем бесплатный аудит отдела продаж:", reply_markup=inline_kb
    )

# Обработка нажатия кнопки "✅ Да, хочу аудит"
# Обработка нажатия кнопки "✅ Да, хочу аудит"
async def handle_audit_request(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()  # Убираем уведомление о нажатии кнопки

    # Отправляем сообщение пользователю
    await bot.send_message(callback.from_user.id, "Отлично! Наш эксперт свяжется с вами в течение дня 📞")
    
    # Получаем данные пользователя
    user_id = callback.from_user.id
    username = callback.from_user.username  # Username из Telegram
    first_name = callback.from_user.first_name  # Имя из Telegram

    # Открываем первый лист для поиска данных
    sheet1 = init_gspread().sheet1  # Первый лист
    records = sheet1.get_all_records()

    # Ищем данные по username
    user_data = None
    for record in records:
        if record['username'] == username:  # Ищем запись по username
            user_data = record
            break

    # Если данные найдены, извлекаем номер телефона
    if user_data:
        userphone = user_data.get('userphone', 'Нет данных')  # Номер телефона
        first_name = user_data.get('first_name', 'Нет данных')  # Имя из контакта
    else:
        userphone = 'Нет данных'
        first_name = 'Нет данных'

    # Открываем второй лист для записи данных
    sheet2 = init_gspread().get_worksheet(1)  # Второй лист (индекс 1)
    
    # Получаем текущую дату
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Записываем данные во второй лист
    sheet2.append_row([username, first_name, userphone, current_date, "Высокая"])  # Добавляем данные в новую строку

# Обработка нажатия кнопки "❌ Нет, позже"
async def handle_later_request(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()  # Убираем уведомление о нажатии кнопки
    await asyncio.sleep(5)  # Ждем 48 часов (172800 секунд)
    
    await bot.send_message(callback.from_user.id, 
        "Посмотрите еще один короткий кейс, как похожая компания перестала сливать лиды и выросла на 25% за 1 месяц: https://rutube.ru/video/3a0ee47db8e2e0f8a75001fbe618fdd3/\n"
        "Если решитесь на аудит, напишите мне любое сообщение! 😉"
    )

# Регистрация всех обработчиков
def reg_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(contact_handler, F.contact)
    dp.callback_query.register(handle_audit_request, F.data == "want_audit")
    dp.callback_query.register(handle_later_request, F.data == "later")