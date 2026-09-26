import asyncio
import os
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

from fastapi import FastAPI


TOKEN = process.env.BOT_ID
WEB_APP_URL = process.env.PROJECT_URL


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    chat_id = message.chat.id

    print(f"🚀 START FROM: {chat_id}", flush=True)
    print(f"📌 CHAT ID: {chat_id}", flush=True)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть веб-приложение",
                    web_app=WebAppInfo(url=WEB_APP_URL),
                )
            ]
        ]
    )

    await message.answer(
        f"Ваш Telegram ID: {chat_id}\n\n"
        "Нажмите кнопку ниже, чтобы открыть веб-приложение:",
        reply_markup=keyboard,
    )


@dp.message(Command("id"))
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id

    print(f"📌 CHAT ID: {chat_id}", flush=True)

    await message.answer(
        f"Ваш Telegram ID: {chat_id}"
    )


async def run_polling():
    try:
        print("🚀 Telegram polling starting...", flush=True)

        # Если раньше использовался webhook,
        # удаляем его перед запуском polling.
        await bot.delete_webhook(drop_pending_updates=True)

        print("✅ Webhook deleted", flush=True)
        print("👂 Polling is running...", flush=True)

        await dp.start_polling(bot)

    except Exception as error:
        print(f"❌ POLLING ERROR: {error}", flush=True)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FASTAPI LIFESPAN START", flush=True)

    polling_task = asyncio.create_task(
        run_polling()
    )

    yield

    print("🛑 Stopping Telegram polling...", flush=True)

    polling_task.cancel()

    try:
        await polling_task
    except asyncio.CancelledError:
        pass

    await bot.session.close()

    print("✅ Bot stopped", flush=True)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "message": "Бот работает!",
        "telegram_polling": "running",
    }
