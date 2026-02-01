from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.inline import products_inline

router = Router()

@router.message(lambda msg: msg.text == "🛍 Mahsulotlar")
async def show_products(message: Message, db):
    products = await db.get_products()
    await message.answer(
        "🛍 Mahsulotlar:",
        reply_markup=products_inline(products)
    )


@router.callback_query(lambda c: c.data.startswith("product_"))
async def product_detail(callback: CallbackQuery):
    product_id = callback.data.split("_")[1]
    await callback.message.answer(
        f"📦 Mahsulot ID: {product_id}\n"
        f"(Keyin batafsil info + savatchaga qo‘shish qilamiz)"
    )
    await callback.answer()
