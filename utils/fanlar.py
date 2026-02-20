from openpyxl import load_workbook

async def get_test_questions(file_path: str) -> list[dict]:
    wb = load_workbook(file_path)
    sheet = wb.active
    questions = []
    for row in sheet.iter_rows(min_row=1, max_col=30, values_only=True):
        if row[0]:
            questions.append({
                "question": row[0],
                "options": row[1:5],
                "answer": row[5]
            })
    return questions