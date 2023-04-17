from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.markdown import hspoiler

from buttons import choosing_for_cards_mode_cb, \
    categories_with_id_buttons, user_home_buttons, cards_slider_buttons, cards_slider_cb
from config import dp
from states import CardPractice
from storage.models import User, Note, NoteCategory


@dp.callback_query_handler(text="cards_mode")
async def choose_category_cards(call: CallbackQuery, user: User):
    note_names = await Note.objects.get_names(user)
    if not note_names:
        return await call.message.edit_text(
            "<b>Для данного режима необходимо наличие минимум "
            "1 категории и 1 незавершенной заметки</b>",
            reply_markup=user_home_buttons
        )
    
    await CardPractice.input_category.set()
    await call.message.edit_text(
        "<b>Выберите категорию для практики</b>",
        reply_markup=await categories_with_id_buttons(
            await user.categories.all(),
            choosing_for_cards_mode_cb
        )
    )


@dp.callback_query_handler(choosing_for_cards_mode_cb.filter(), state=CardPractice.input_category)
async def remove_category(call: CallbackQuery, callback_data: dict, state: FSMContext, user: User):
    category_id = int(callback_data.get("category_id"))
    category = await NoteCategory.objects.get(id=category_id)
    category_notes = await category.notes.all()
    
    if not category_notes:
        return await call.message.edit_text(
            "<b>В выбранной категории нет заметок</b>",
            reply_markup=await categories_with_id_buttons(
                await user.categories.all(),
                choosing_for_cards_mode_cb
            )
        )
    await CardPractice.viewing.set()
    await state.update_data(category_notes=list(category_notes))
    await show_selected_slide(call, state)


@dp.callback_query_handler(cards_slider_cb.filter(), state=CardPractice.viewing)
async def show_selected_slide(call: CallbackQuery, state: FSMContext,
                              callback_data: dict | None = None):
    state_data = await state.get_data()
    card_index = await _parse_card_index_from_cb(callback_data, state_data)
    
    await state.update_data(current_card_index=card_index)
    
    number_of_cards = len(state_data.get("category_notes"))
    position = f"{card_index + 1} / {number_of_cards}"
    
    markup = await cards_slider_buttons(
        current_card_index=card_index, cards_total=number_of_cards
    )
    await format_and_show_card(call, state_data["category_notes"][card_index], position, markup)


async def _parse_card_index_from_cb(callback_data: dict, state_data: dict):
    card_index = 0
    
    if callback_data and callback_data.get("direction") == "next":
        card_index = (state_data.get("current_card_index", 0) + 1)
    
    if callback_data and callback_data.get("direction") == "previous":
        card_index = state_data.get("current_card_index", 0) - 1
    
    return card_index


async def format_and_show_card(
        call: CallbackQuery, card: Note,
        position: str, markup: InlineKeyboardMarkup | None = None,
):
    caption = f"<b># {position}\n{card.name}</b>\n\n{hspoiler(card.content) if card.content else ''}"
    await call.message.edit_text(caption, reply_markup=markup)
