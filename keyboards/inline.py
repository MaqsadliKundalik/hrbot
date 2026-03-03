from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_keyboard_builder(buttons: list[tuple[str, str]]):
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    return builder.as_markup()

teacher_position_btn = inline_keyboard_builder(
    [
        ("Asosiy ustoz", "position_asosiy"),
        ("Yordamchi ustoz", "position_yordamchi"),
    ]
)