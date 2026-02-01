from aiogram import Router
from aiogram.types import Message
from aiogram import F
from filters.role import RoleFilter
from keyboards import inline,reply
from aiogram.types import CallbackQuery

router = Router()

@router.message(F.text==("👑 Admin panel"), RoleFilter("admin"))
async def admin_panel(message: Message):
    await message.answer("👑 Admin panel", reply_markup=reply.admin_panel_menu())


@router.message(F.text==("⬅️ Orqaga"), RoleFilter("admin"))
async def back_to_user_menu(message: Message):
    await message.answer("Asosiy menu", reply_markup=reply.admin_menu())

@router.message(F.text==("👥 Userlar"), RoleFilter("admin"))
async def show_users(message: Message, db):
    users = await db.get_users()

    if not users:
        await message.answer("Userlar yo‘q")
        return

    await message.answer(
        "👥 Userlar ro‘yxati:",
        reply_markup=inline.users_inline(users)
    )

@router.callback_query(lambda c: c.data.startswith("user_"),RoleFilter("admin"))
async def choose_role(callback: CallbackQuery):
    telegram_id = callback.data.split("_")[1]

    await callback.message.answer(
        "🔄 Role tanlang:",
        reply_markup=inline.role_inline(telegram_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("setrole_"),RoleFilter("admin"))
async def set_role(callback: CallbackQuery, db):
    _, role, telegram_id = callback.data.split("_")

    await db.set_user_role(
        telegram_id=int(telegram_id),
        role=role
    )

    await callback.message.edit_text(
        f"✅ User roli `{role}` ga o‘zgartirildi"
    )
    await callback.answer("Role yangilandi")

