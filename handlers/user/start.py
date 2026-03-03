from database.models import TgUser
from aiogram import Router, F
from aiogram.types import Message
from filters.user import IsRegisteredUser
from aiogram.filters import CommandStart
from keyboards.reply import main_menu_users_btn, vacancies_btn
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart(), IsRegisteredUser())
async def start(message: Message):  
    await message.answer("Sizni yana ko'rib turganimdan hursandman!", reply_markup=main_menu_users_btn(is_registered=True))

@router.message(F.text == "Vakansiyalar", IsRegisteredUser())
async def vacancies(message: Message):  
    await message.answer("Vakansiya turini tanlang.", reply_markup=vacancies_btn)

@router.message(F.text == "Biz haqimizda")
async def about(message: Message):  
    await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=1003848271662, message_id=6)

@router.message(F.text == "Bog'lanish")
async def contact(message: Message):  
    await message.answer("Biz bilan bog'lanish uchun")

@router.message(F.text == "Orqaga")
async def back(message: Message, state: FSMContext):
    exists = await TgUser.get_or_none(tg_id=message.chat.id)
    if exists:
        await message.answer("Orqaga qaytdik!!", reply_markup=main_menu_users_btn(is_registered=True))
    else:
        await message.answer("Orqaga qaytdik!!", reply_markup=main_menu_users_btn(is_registered=False))
    await state.clear()
