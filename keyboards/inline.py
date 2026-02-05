from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def products_inline(products):
    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"adminproduct_{product['id']}"
            )
        ])
        

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def admin_product_actions(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Update",
                    callback_data=f"adminupdate_{product_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=f"admindelete_{product_id}"
                )
            ]
        ]
    )

def product_actions(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Savatcha qoshish",
                    callback_data=f"savatcha_{product_id}"
                )
                
            ]
        ]
    )


def users_inline(users):
    keyboard = []

    for user in users:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{user['full_name']} ({user['role']})",
                callback_data=f"user_{user['telegram_id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def role_inline(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👑 Admin",
                    callback_data=f"setrole_admin_{telegram_id}"
                ),
                InlineKeyboardButton(
                    text="👤 User",
                    callback_data=f"setrole_user_{telegram_id}"
                )
            ]
        ]
    )

