from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from database.models import AdminsResume, TeacherResume, TgUser, QuizAnswers, Quizs
import io
from collections import defaultdict


HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill(start_color="2E4057", end_color="2E4057", fill_type="solid")
ALT_FILL = PatternFill(start_color="F2F7FF", end_color="F2F7FF", fill_type="solid")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)


def _style_header_row(ws, row: int, col_count: int):
    for col in range(1, col_count + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = THIN_BORDER


def _style_data_row(ws, row: int, col_count: int):
    fill = ALT_FILL if row % 2 == 0 else None
    for col in range(1, col_count + 1):
        cell = ws.cell(row=row, column=col)
        if fill:
            cell.fill = fill
        cell.alignment = LEFT
        cell.border = THIN_BORDER


def _set_column_widths(ws, widths: list):
    for i, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 30


def _safe_sheet_title(title: str) -> str:
    """Excel sheet nomi 31 belgidan oshmasligi va maxsus belgilar bo'lmasligi kerak."""
    for ch in r'\/*?:[]\r\n':
        title = title.replace(ch, " ")
    return title[:31]


async def generate_report() -> io.BytesIO:
    wb = Workbook()
    # Birinchi bo'sh sheetni keyinroq o'chirish uchun saqlab qo'yamiz
    default_sheet = wb.active

    # ── AdminsResume: har bir job uchun alohida sheet ─────────────────────────
    admin_headers = [
        "№", "Telegram ID", "Ism Familiya", "Telefon", "Tug'ilgan sana",
        "Xorijiy til", "Til darajasi",
        "Tajriba", "Ish vaqti",
        "Oxirgi ish joyi", "Ketish sababi", "Oxirgi ish joyi telefoni",
        "Ariza sanasi",
    ]
    admin_widths = [5, 18, 25, 18, 15, 18, 15, 15, 15, 25, 25, 22, 20]

    admins = await AdminsResume.all().prefetch_related("user").order_by("job", "id")

    # job bo'yicha guruhlash
    admin_groups: dict[str, list] = defaultdict(list)
    for resume in admins:
        admin_groups[resume.job].append(resume)

    for job, resumes in admin_groups.items():
        ws = wb.create_sheet(title=job)
        ws.append(admin_headers)
        _style_header_row(ws, 1, len(admin_headers))
        _set_column_widths(ws, admin_widths)

        for idx, resume in enumerate(resumes, start=1):
            user: TgUser = resume.user
            phones = ", ".join(v for v in user.phone_numbers.values() if v) if user.phone_numbers else "-"
            row_data = [
                idx,
                user.tg_id,
                user.full_name,
                phones,
                str(user.birth_date) if user.birth_date else "-",
                resume.foreign_language,
                resume.foreign_language_level,
                resume.experience,
                resume.working_time,
                resume.last_work_place,
                resume.why_leave_work,
                resume.last_work_place_phone,
                resume.created_at.strftime("%d.%m.%Y %H:%M") if resume.created_at else "-",
            ]
            ws.append(row_data)
            _style_data_row(ws, idx + 1, len(admin_headers))

    # ── TeacherResume: har bir subject uchun alohida sheet ───────────────────
    teacher_headers = [
        "№", "Telegram ID", "Ism Familiya", "Telefon", "Tug'ilgan sana",
        "Tajriba", "Ish vaqti", "Maosh (so'm)",
        "Sertifikatlar",
        "Oxirgi ish joyi", "Ketish sababi", "Oxirgi ish joyi telefoni",
        "Ariza sanasi",
    ]
    teacher_widths = [5, 18, 25, 18, 15, 15, 15, 18, 35, 25, 25, 22, 20]

    teachers = await TeacherResume.all().prefetch_related("user").order_by("subject", "id")

    # subject bo'yicha guruhlash
    teacher_groups: dict[str, list] = defaultdict(list)
    for resume in teachers:
        teacher_groups[resume.subject].append(resume)

    for subject, resumes in teacher_groups.items():
        ws = wb.create_sheet(title=subject)
        ws.append(teacher_headers)
        _style_header_row(ws, 1, len(teacher_headers))
        _set_column_widths(ws, teacher_widths)

        for idx, resume in enumerate(resumes, start=1):
            user: TgUser = resume.user
            phones = ", ".join(v for v in user.phone_numbers.values() if v) if user.phone_numbers else "-"
            certs = (
                "\n".join(
                    f"{s.get('name', '?')} — {s.get('ball', '?')}"
                    for s in resume.sertificates
                )
                if resume.sertificates
                else "-"
            )
            row_data = [
                idx,
                user.tg_id,
                user.full_name,
                phones,
                str(user.birth_date) if user.birth_date else "-",
                resume.experience,
                resume.working_time,
                resume.salary,
                certs,
                resume.last_work_place,
                resume.why_leave_work,
                resume.last_work_place_phone,
                resume.created_at.strftime("%d.%m.%Y %H:%M") if resume.created_at else "-",
            ]
            ws.append(row_data)
            _style_data_row(ws, idx + 1, len(teacher_headers))

    # ── Test natijalari ───────────────────────────────────────────────────────
    ws_quizzes = wb.create_sheet(title="Test natijalari")

    quiz_headers = [
        "№", "Telegram ID", "Ism Familiya", "Fan", "To'g'ri javoblar",
    ]
    quiz_widths = [5, 18, 25, 25, 18]

    ws_quizzes.append(quiz_headers)
    _style_header_row(ws_quizzes, 1, len(quiz_headers))
    _set_column_widths(ws_quizzes, quiz_widths)

    quiz_answers = (
        await QuizAnswers.all()
        .prefetch_related("user", "quiz", "quiz__subject")
        .order_by("id")
    )
    for idx, answer in enumerate(quiz_answers, start=1):
        user: TgUser = answer.user
        quiz: Quizs = answer.quiz
        subject_name = quiz.subject.name if quiz.subject else "-"
        row_data = [
            idx,
            user.tg_id,
            user.full_name,
            subject_name,
            answer.correct_answers,
        ]
        ws_quizzes.append(row_data)
        _style_data_row(ws_quizzes, idx + 1, len(quiz_headers))

    # Dastlabki bo'sh sheetni o'chirish
    wb.remove(default_sheet)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
