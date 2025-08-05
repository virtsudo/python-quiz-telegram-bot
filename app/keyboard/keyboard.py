from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ResCallbackFab(CallbackData, prefix="correct"):
    action: str


def keyboard_gen(buttons: list[str]) -> ReplyKeyboardMarkup:
    keyboard_buttons = [KeyboardButton(text=button) for button in buttons]
    return ReplyKeyboardMarkup(keyboard=[keyboard_buttons], resize_keyboard=True)


def inline_keyboard_gen(buttons: list[str]) -> InlineKeyboardButton:
    buttons = buttons[1:len(buttons)-1].split(", ")
    buttons = [i[1:len(i)-1] for i in buttons]
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(text=button[4:], callback_data=ResCallbackFab(action=button[4:]))
    builder.adjust(2)
    return builder.as_markup()
