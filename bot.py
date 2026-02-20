from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from handlers import router as main_router
from logging import basicConfig, INFO
from database import init_db, close_db
from miidlewares.base import LongMessageMiddleware

dp = Dispatcher()

async def main():
    bot = Bot(token=BOT_TOKEN)

    dp.include_router(main_router)
    dp.update.middleware(LongMessageMiddleware())

    await init_db()
    try:
        await dp.start_polling(bot)
    finally:
        await close_db()

if __name__ == "__main__":
    import asyncio
    basicConfig(level=INFO)
    asyncio.run(main())
