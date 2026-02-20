import re

def is_valid_phone(phone: str) -> bool:
    # O'zbekiston telefon raqami formatlari: +998 90 123 45 67, +998901234567, 998901234567
    pattern = r"^(\+998|998)?\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$"
    return re.match(pattern, phone) is not None

def is_valid_date(date: str) -> bool:
    # O'zbekiston sana formatlari: dd.mm.yyyy, dd/mm/yyyy, dd-mm-yyyy
    pattern = r"^\d{2}[./-]\d{2}[./-]\d{4}$"
    return re.match(pattern, date) is not None
