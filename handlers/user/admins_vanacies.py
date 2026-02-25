from aiogram import Router, F
from aiogram.types import Message
from filters.user import IsRegisteredUser
from aiogram.fsm.context import FSMContext
from keyboards.reply import kasblar_lst_btn, working_time_btn, back_btn, main_menu_users_btn, vacancies_btn
from database.models import VacanciesText, Subjects, AdminsResume, TgUser, VacanciesText
from states.user import AdminsVacancyState
from filters.user import InAdminsResumeState
from utils import is_valid_phone

router = Router()

@router.message(F.text == "Orqaga", InAdminsResumeState())
async def admins_vanacies(message: Message, state: FSMContext):

    match await state.get_state():
        case AdminsVacancyState.vacancy_type:
            await message.answer("Ortga qaytildi.", reply_markup=vacancies_btn)
            await state.clear()
            return
        case AdminsVacancyState.working_time:
            await admins_vanacies_start(message, state)
        case AdminsVacancyState.foreign_language:
            await message.answer("Ish vaqtini tanlang:", reply_markup=working_time_btn)
            await state.set_state(AdminsVacancyState.working_time)
        case AdminsVacancyState.foreign_language_level:
            await message.answer("Qaysi xorijiy tillarni bilasiz?", reply_markup=back_btn)
            await state.set_state(AdminsVacancyState.foreign_language)
        case AdminsVacancyState.experience:
            await admins_vanacies_foreign_language(message, state)
        case AdminsVacancyState.last_work_place:
            await admins_vanacies_foreign_language_level(message, state)
        case AdminsVacancyState.why_leave_work:
            await admins_vanacies_experience(message, state)
        case AdminsVacancyState.last_work_place_phone:
            await admins_vanacies_last_work_place(message, state)

@router.message(F.text == "Adminlarga", IsRegisteredUser())
async def admins_vanacies_start(message: Message, state: FSMContext):
    kasblar = await VacanciesText.exclude(name__in=[sub.name for sub in await Subjects.all()])
    if not kasblar:
        await message.answer("Hozirda adminlarga vakansiya mavjud emas!")
        return

    await message.answer("Vakansiyani tanlang:", reply_markup=kasblar_lst_btn(kasblar=[kasb.name for kasb in kasblar], is_admin=False))
    await state.set_state(AdminsVacancyState.vacancy_type)

@router.message(F.text, AdminsVacancyState.vacancy_type)
async def admins_vanacies_vacancy_type(message: Message, state: FSMContext):
    if message.text not in [kasb.name for kasb in await VacanciesText.exclude(name__in=[sub.name for sub in await Subjects.all()])]:
        await message.answer("Bunday vakansiya mavjud emas!")
        return
    await state.update_data(vacancy_type=message.text)
    vacansy_text = await VacanciesText.get_or_none(name=message.text)
    if vacansy_text:
        await message.answer(vacansy_text.text, parse_mode="HTML")
    await message.answer("Ish vaqtini tanlang:", reply_markup=working_time_btn)
    await state.set_state(AdminsVacancyState.working_time)

@router.message(F.text, AdminsVacancyState.working_time)
async def admins_vanacies_working_time(message: Message, state: FSMContext):
    if message.text in ["09:00 - 20:00", "08:00 - 17:00", "14:00 - 20:00", "08:00 - 20:00"]:
        await state.update_data(working_time=message.text)
        await message.answer("Qaysi xorijiy tillarni bilasiz?", reply_markup=back_btn)
        await state.set_state(AdminsVacancyState.foreign_language)
    else:
        await message.answer("Bunday ish vaqti mavjud emas!")

@router.message(F.text, AdminsVacancyState.foreign_language)
async def admins_vanacies_foreign_language(message: Message, state: FSMContext):
    await state.update_data(foreign_language=message.text)
    await message.answer("Xorijiy tillarni bilish darajangizni kiriting.", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.foreign_language_level)

@router.message(F.text, AdminsVacancyState.foreign_language_level)
async def admins_vanacies_foreign_language_level(message: Message, state: FSMContext):
    await state.update_data(foreign_language_level=message.text)
    await message.answer("Sohadagi tajribangiz necha yil?", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.experience)

@router.message(F.text, AdminsVacancyState.experience)
async def admins_vanacies_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Oxirgi ish joyingiz qayer edi?", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.last_work_place)

@router.message(F.text, AdminsVacancyState.last_work_place)
async def admins_vanacies_last_work_place(message: Message, state: FSMContext):
    await state.update_data(last_work_place=message.text)
    await message.answer("Oxirgi ish joyingizdan ketish sababini kiriting", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.why_leave_work)

@router.message(F.text, AdminsVacancyState.why_leave_work)
async def admins_vanacies_why_leave_work(message: Message, state: FSMContext):
    await state.update_data(why_leave_work=message.text)
    await message.answer("Oxirgi ish joyingiz telefon raqami?", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.last_work_place_phone)

@router.message(F.text, AdminsVacancyState.last_work_place_phone)
async def admins_vanacies_last_work_place_phone(message: Message, state: FSMContext):
    if is_valid_phone(message.text):
        state_data = await state.get_data()
        user = await TgUser.get_or_none(tg_id=message.from_user.id)
        await AdminsResume.create(
            user=user,
            job=state_data["vacancy_type"],
            working_time=state_data["working_time"],
            foreign_language=state_data["foreign_language"],
            foreign_language_level=state_data["foreign_language_level"],
            experience=state_data["experience"],
            last_work_place=state_data["last_work_place"],
            why_leave_work=state_data["why_leave_work"],
            last_work_place_phone=message.text,
        )
        await message.answer("""
Sabr bilan shu joyigacha kelganingiz uchun raxmat! Siz birinchi bosqichdan muvaffaqiyatli o'tdingiz.

Tez orada siz bilan bog'lanamiz!
        """, reply_markup=main_menu_users_btn(is_registered=True))
        await state.clear()
    else:
        await message.answer("Noto'g'ri telefon raqami! To'g'ri telefon raqam kiriting.\n\nMasalan, +998 90 123 45 67")