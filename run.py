import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from app.db import init_db
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.handlers import router
from config import TOKEN
from app.language import language_data

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    init_db()
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')