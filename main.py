from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Бот работает!"}


TOKEN = "НОВЫЙ_ТОКЕН_ОТ_BOTFATHER"
WEB_APP_URL = "https://weddinglanding-six.vercel.app/"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    print("CHAT ID:", message.chat.id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть веб-приложение",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )

    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть веб-приложение:",
        reply_markup=keyboard
    )


@dp.message(Command("id"))
async def get_chat_id(message: types.Message):
    print("CHAT ID:", message.chat.id)

    await message.answer(
        f"Ваш Telegram ID: {message.chat.id}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())