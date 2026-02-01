from aiogram import Router
from aiogram.types import Message
router = Router()



@router.message(lambda msg: msg.text == "📦 Buyurtmalarim")
async def my_orders(message: Message):
    await message.answer("Sizning buyurtmalaringiz:")

@router.message(lambda msg: msg.text == "👤 Profil")
async def profile(message: Message, db):
    user = await db.get_user_by_telegram_id(message.from_user.id)
    await message.answer(
        f"👤 Profil\n\n"
        f"Ism: {user['full_name']}\n"
        f"Telefon: {user['phone']}\n"
        f"Role: {user['role']}"
    )
