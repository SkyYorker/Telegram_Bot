from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        
        # Передаем в callback_data информацию о выбранном варианте
        callback_data = f"right_answer_{option}" if option == right_answer else f"wrong_answer_{option}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data)
        )

    builder.adjust(1)
    return builder.as_markup()


def clean_stat_keyboard():
    # Создаем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="reset_yes"),
            InlineKeyboardButton(text="Нет", callback_data="reset_no")
        ]
    ])

    return keyboard