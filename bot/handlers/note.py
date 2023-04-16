from typing import Iterable

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from buttons import cancel_button, categories_with_id_buttons, \
    mark_as_category_cb, user_home_buttons
from config import dp
from states import NoteOperation
from storage.models import User, Note


@dp.callback_query_handler(text="add_note")
async def start_adding_note_process(call: CallbackQuery, user: User):
    user_categories = await user.categories.all()
    if not user_categories:
        return await call.message.edit_text(
            "Перед добавлением заметки необходимо создать категорию",
            reply_markup=user_home_buttons
        )
    await call.message.edit_text(
        "<b>Введите название заметки</b>\n\n"
        "Примеры 👇🏻\n<code>Употребление a и an</code>\n<code>Кто такие лиды?</code>",
        reply_markup=cancel_button
    )
    await NoteOperation.input_name.set()


async def _note_name_is_valid(name: str, note_names: Iterable[str]):
    return len(name) < 128 and (name not in note_names)


@dp.message_handler(content_types=["text"], state=NoteOperation.input_name)
async def keep_note_name(message: Message, user: User, state: FSMContext):
    added_note_names = await Note.objects.get_names(user)
    
    if not await _note_name_is_valid(message.text, added_note_names):
        return await message.answer(
            "<b>Название заметки невалидно, введите заново\n\nТребования 👇🏻</b>\n"
            "✔️ Уникальность\n"
            "✔️ До 128 символов",
            reply_markup=cancel_button
        )
    await state.update_data(name=message.text)
    await NoteOperation.input_content.set()
    await message.answer("Теперь введите содержание заметки")


@dp.message_handler(content_types=["text"], state=NoteOperation.input_content)
async def keep_note_content(message: Message, user: User, state: FSMContext):
    user_categories = await user.categories.all()
    await state.update_data(content=message.text)
    await NoteOperation.input_category.set()
    await message.answer(
        "Осталось выбрать категорию заметки",
        reply_markup=await categories_with_id_buttons(
            user_categories, mark_as_category_cb
        )
    )


@dp.callback_query_handler(mark_as_category_cb.filter(), state=NoteOperation.input_category)
async def save_note(call: CallbackQuery, state: FSMContext, callback_data: dict, user: User):
    state_data = await state.get_data()
    category_id = int(callback_data.get("category_id"))
    await state.finish()
    
    await Note.objects.create(
        name=state_data.get("name"),
        creator=user,
        content=state_data.get("content"),
        category=category_id
    )
    await call.message.edit_text(
        "<b>Заметка сохранена ✔️</b>\n\n"
        "Первое напоминание придёт ~ через 19 минут",
        reply_markup=user_home_buttons
    )
    await state.finish()
