import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import types
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from keyboards import kb_con

# Настройка доступа к Google Sheets
def init_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/klim-petrov/projects/smartTG/credentials.json", scope)  # Укажите путь к вашему JSON-файлу
    client = gspread.authorize(creds)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1K6PkCuSYepOhKzk5sfm8YCxsJ8pxGBfi8IuH1VgxPIY/edit#gid=0").sheet1  # Откройте вашу таблицу

async def cmd_start(message: types.Message):
    await message.answer(f"Привет! 👋\nЧтобы получить PDF-гайд «Как увеличить продажи отдела на 30% с помощью ИИ-ассистента», нажмите кнопку ниже и поделитесь вашим контактом:", parse_mode="HTML", reply_markup=kb_con)

async def contact_handler(message: types.Message):
    contact = message.contact
    await message.answer(f"Спасибо! Гайд уже у вас 📩\nЗавтра вернусь и узнаю ваше мнение 😉", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

    # Сохраняем контакт в Google Sheets
    sheet = init_gspread()
    sheet.append_row([contact.first_name, contact.phone_number])  # Добавляем данные в новую строку

    # Отправляем PDF-файл
    pdf_file = FSInputFile("/home/klim-petrov/projects/smartTG/guide.pdf")  # Укажите путь к вашему PDF-файлу
    await message.answer_document(pdf_file)

# Регистрация всех обработчиков
def reg_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(contact_handler, F.contact)