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

@router.message(F.text == "Biz haqimizda", IsRegisteredUser())
async def about(message: Message):  
    await message.answer("Biz haqimizda")

@router.message(F.text == "Bog'lanish", IsRegisteredUser())
async def contact(message: Message):  
    await message.answer("Biz bilan bog'lanish uchun")

@router.message(F.text == "Orqaga", IsRegisteredUser())
async def back(message: Message, state: FSMContext):
    await message.answer("Orqaga qaytdik!!", reply_markup=main_menu_users_btn(is_registered=True))
    await state.clear()
