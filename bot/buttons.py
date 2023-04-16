from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from storage.models import NoteCategory

try_app_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Хмм, давай попробуем 🔥", callback_data="try_app"),
)

user_home_buttons = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Категории Заметок", callback_data="note_categories"),
    InlineKeyboardButton("Добавить Заметку", callback_data="add_note"),
).row(
    InlineKeyboardButton("Мод «Карточки»", callback_data="cards_mod"),
).row(
    InlineKeyboardButton("Как это устроено?", callback_data="about_mind"),
)

manage_categories_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Добавить Категорию", callback_data="add_category"),
    InlineKeyboardButton("Удалить Категорию", callback_data="remove_category"),
    InlineKeyboardButton("Назад", callback_data="cancel"),
)

remember_note_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Запомнил, больше не отправлять", callback_data="mark_note_as_remember"),
)

cancel_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Отмена", callback_data="cancel"),
)

choosing_for_removing_cb = CallbackData("choosing_for_removing", "category_id")

mark_as_category_cb = CallbackData("mark_as_category", "category_id")


async def categories_with_id_buttons(categories: Iterable[NoteCategory], cb: CallbackData):
    buttons = InlineKeyboardMarkup(row_width=3)
    
    buttons.add(InlineKeyboardButton("Назад", callback_data="cancel"))
    for cat in categories:
        buttons.add(
            InlineKeyboardButton(
                cat.name.title(),
                callback_data=cb.new(category_id=cat.id)
            )
        )
    
    return buttons
