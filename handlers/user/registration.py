from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.registration import RegistrationState
from keyboards.reply import user_menu,admin_menu
# from database.db import Database as db
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext,db):
    exists = await db.user_exists(telegram_id=message.from_user.id)
    # ❗ Agar oldin ro‘yxatdan o‘tgan bo‘lsa
    if exists:
        role = await db.get_user_role(message.from_user.id)

        if role.lower() == "admin":
            await message.answer(
                "ℹ️ Siz allaqachon ro‘yxatdan o‘tgansiz",
                reply_markup=admin_menu()
            )
        else:
            await message.answer(
                "ℹ️ Siz allaqachon ro‘yxatdan o‘tgansiz",
                reply_markup=user_menu()
            )
        return  # FSM boshlanmaydi

    # ❗ Yangi user bo‘lsa
    await message.answer("Ismingizni kiriting:")
    await state.set_state(RegistrationState.full_name)


@router.message(RegistrationState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(RegistrationState.phone)


@router.message(RegistrationState.phone)
async def get_phone(message: Message, state: FSMContext, db):
    data = await state.get_data()

    await db.add_user(
        telegram_id=message.from_user.id,
        full_name=data["full_name"],
        phone=message.text
    )

    role = await db.get_user_role(message.from_user.id)

    await state.clear()

    if role == "admin":
        await message.answer(
            "👑 Admin sifatida tizimga kirdingiz",
            reply_markup=admin_menu()
        )
    else:
        await message.answer(
            "✅ Ro‘yxatdan o‘tdingiz!",
            reply_markup=user_menu()
        )
