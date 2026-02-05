from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.product import AddProductState,UpdateProductState
from filters.role import RoleFilter
from keyboards.inline import product_actions,admin_product_actions
from keyboards.inline import products_inline

router = Router()


@router.message(F.text==("➕ Mahsulot qo‘shish"), RoleFilter("admin"))
async def add_product_start(message: Message, state: FSMContext):
    await message.answer("📦 Mahsulot nomini kiriting:")
    await state.set_state(AddProductState.name)

@router.message(AddProductState.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(AddProductState.price)

@router.message(AddProductState.price)
async def add_product_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Narx faqat son bo‘lishi kerak")
        return

    await state.update_data(price=int(message.text))
    await message.answer("📝 Tavsifini kiriting:")
    await state.set_state(AddProductState.description)


@router.message(AddProductState.description)
async def add_product_finish(message: Message, state: FSMContext, db):
    data = await state.get_data()

    await db.add_product(
        name=data["name"],
        price=data["price"],
        description=message.text
    )
    

    await message.answer("Yangilandi")
    await state.clear()




@router.message(F.text==("📋 Mahsulotlar(Admin)"), RoleFilter("admin"))
async def show_products(message: Message, db):
    products = await db.get_products()

    if not products:
        await message.answer("📭 Mahsulotlar mavjud emas")
        return

    await message.answer(
        "📦 Mahsulotlar ro‘yxati:",
        reply_markup=products_inline(products)
    )

@router.callback_query(lambda c: c.data.startswith("adminproduct_"),RoleFilter("admin"))
async def product_detail(callback: CallbackQuery, db):
    product_id = int(callback.data.split("_")[1])

    product = await db.get_product(product_id)

    text = (
        f"📦 {product['name']}\n"
        f"💰 {product['price']} so‘m\n\n"
        f"{product['description']}"
    )

    await callback.message.answer(
        text,
        reply_markup=admin_product_actions(product_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("admindelete_"),RoleFilter('admin'))
async def delete_product(callback: CallbackQuery, db):
    product_id = int(callback.data.split("_")[1])

    await db.delete_product(product_id)

    await callback.message.edit_text("🗑 Mahsulot o‘chirildi")
    await callback.answer()




@router.callback_query(F.data.startswith("adminupdate_"), RoleFilter("admin"))
async def add_product_start(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])
    await state.update_data(product_id=product_id)
    await call.message.answer("📦 Mahsulot nomini kiriting:")
    await state.set_state(UpdateProductState.name)

@router.message(UpdateProductState.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(UpdateProductState.price)

@router.message(UpdateProductState.price)
async def add_product_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Narx faqat son bo‘lishi kerak")
        return

    await state.update_data(price=int(message.text))
    await message.answer("📝 Tavsifini kiriting:")
    await state.set_state(UpdateProductState.description)


@router.message(UpdateProductState.description)
async def add_product_finish(message: Message, state: FSMContext, db):
    data = await state.get_data()

    await db.update_product(
        name=data["name"],
        price=data["price"],
        description=message.text,
        product_id=data["product_id"]
    )

    await message.answer("Mahsulot yangilandi")
    await state.clear()
