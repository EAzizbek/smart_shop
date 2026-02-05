from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.inline import products_inline,product_actions
from filters.role import RoleFilter

router = Router()

@router.message(lambda msg: msg.text == "🛍 Mahsulotlar")
async def show_products(message: Message, db):
    products = await db.get_products()
    await message.answer(
        "🛍 Mahsulotlar:",
        reply_markup=products_inline(products)
    )


@router.callback_query(lambda c: c.data.startswith("adminproduct_"),RoleFilter("user"))
async def product_detail(callback: CallbackQuery,db):
    product_id = int(callback.data.split("_")[1])

    product = await db.get_product(product_id)

    text = (
        f"📦 {product['name']}\n"
        f"💰 {product['price']} so‘m\n\n"
        f"{product['description']}"
    )
    await callback.message.answer(text,reply_markup=product_actions(product_id))
    await callback.answer()
