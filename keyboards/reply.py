from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Mahsulotlar")],
            [KeyboardButton(text="📦 Buyurtmalarim")],
            [KeyboardButton(text="👤 Profil")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Mahsulotlar")],
            [KeyboardButton(text="📦 Buyurtmalarim")],
            [KeyboardButton(text="👤 Profil")],
            [KeyboardButton(text="👑 Admin panel")]
        ],
        resize_keyboard=True
    )

def admin_panel_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mahsulot qo‘shish")],
            [KeyboardButton(text="📋 Mahsulotlar")],
            [KeyboardButton(text="👥 Userlar")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )