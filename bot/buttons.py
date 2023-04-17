from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from config import APP_OVERVIEW_POST
from storage.models import NoteCategory

try_app_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Хмм, давай попробуем 🔥", callback_data="try_app"),
)

user_home_buttons = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Категории", callback_data="note_categories"),
    InlineKeyboardButton("Новая Заметка", callback_data="add_note"),
).row(
    InlineKeyboardButton("Мод «Карточки»", callback_data="cards_mode"),
).row(
    InlineKeyboardButton("Как это устроено?", url=APP_OVERVIEW_POST),
).row(
    InlineKeyboardButton("Buy me a coffee", callback_data="donate"),
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


async def donate_button(invoice_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Оплатить", url=invoice_url),
    )


choosing_for_removing_cb = CallbackData("choosing_for_removing", "category_id")

choosing_for_cards_mode_cb = CallbackData("choosing_for_cards_mode", "category_id")

mark_as_category_cb = CallbackData("mark_as_category", "category_id")


async def categories_with_id_buttons(categories: Iterable[NoteCategory], cb: CallbackData) -> InlineKeyboardMarkup:
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


cards_slider_cb = CallbackData("show_slide", "direction")


async def cards_slider_buttons(current_card_index: int, cards_total: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(row_width=2)
    
    if cards_total >= current_card_index > 0:
        buttons.insert(
            InlineKeyboardButton("◀️", callback_data=cards_slider_cb.new(direction="previous"))
        )
    
    if 0 <= current_card_index < cards_total - 1:
        buttons.insert(
            InlineKeyboardButton("▶️", callback_data=cards_slider_cb.new(direction="next"))
        )
    
    buttons.add(InlineKeyboardButton("Завершить Повторение", callback_data="cancel"))
    return buttons
