from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from filters.role import RoleFilter
router=Router()

@router.callback_query(lambda c: c.data.startswith("savatcha_"),RoleFilter('user'))
async def add_to_cart_handler(callback: CallbackQuery, db):
    product_id = int(callback.data.split("_")[1])
    user_id = await db.get_user_id_by_telegram_id(callback.from_user.id)

    await db.add_to_cart(user_id, product_id)

    await callback.answer("✅ Mahsulot savatchaga qo‘shildi!", show_alert=True)

@router.message(F.text == "🛒 Savatcha")
async def show_cart(message: Message, db):
    user_id = await db.get_user_id_by_telegram_id(message.from_user.id)
    items = await db.get_cart_items(user_id)

    if not items:
        await message.answer("🛒 Savatchangiz bo‘sh")
        return

    text = "🛒 Savatchangiz:\n\n"
    total_sum = 0

    for item in items:
        text += (
            f"📦 {item['name']}\n"
            f"💰 {item['price']} x {item['quantity']} = {item['total']} so‘m\n\n"
        )
        total_sum += item['total']

    text += f"🧾 Jami: {total_sum} so‘m"
    await message.answer(text)

