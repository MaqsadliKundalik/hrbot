import re
from datetime import datetime

def is_valid_phone(phone: str) -> bool:
    # O'zbekiston telefon raqami formatlari: +998 90 123 45 67, +998901234567, 998901234567
    pattern = r"^(\+998|998)?\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$"
    return re.match(pattern, phone) is not None

def is_valid_date(date: str) -> bool:
    # O'zbekiston sana formatlari: dd.mm.yyyy, dd/mm/yyyy, dd-mm-yyyy
    try:
        datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False
