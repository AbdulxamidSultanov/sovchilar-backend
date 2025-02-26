from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command  # Aiogram 3.x
import asyncio
from fastapi import FastAPI

app = FastAPI()  # Render ищет именно эту переменную

@app.get("/")
async def root():
    return {"message": "Бот работает!"}

TOKEN = "8066095257:AAG9W4w2nyg6WKB7zHt1f-CQ8mtQJPis2wM"
WEB_APP_URL = "https://sovchilar-tgapp.vercel.app"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Нажмите кнопку ниже, чтобы открыть веб-приложение:", reply_markup=keyboard)

# Запускаем бота фоновым процессом
loop = asyncio.get_event_loop()
loop.create_task(dp.start_polling(bot))
