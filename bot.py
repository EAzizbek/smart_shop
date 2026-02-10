import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from database.db import Database

from handlers.user.registration import router as reg_router
from handlers.user.menu import router as menu_router
from handlers.user.products import router as product_router
from handlers.admin.panel import router as admin_router
from handlers.admin.product import router as admin_product_router
from handlers.user.cart import router as cart_router



async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database()
    await db.connect()

    dp["db"] = db

    dp.include_router(reg_router)
    dp.include_router(menu_router)
    dp.include_router(product_router)
    dp.include_router(admin_router)
    dp.include_router(admin_product_router)
    dp.include_router(cart_router)


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
