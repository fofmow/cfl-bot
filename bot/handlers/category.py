from typing import Iterable

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from buttons import manage_categories_buttons, categories_with_id_buttons, choosing_for_removing_cb, \
    cancel_button
from config import dp
from states import CategoryOperation
from storage.models import User, NoteCategory
from tools.misc import format_user_added_values


@dp.callback_query_handler(text="note_categories")
async def note_categories_page(call: CallbackQuery, user: User):
    await call.message.delete_reply_markup()
    added_category_names = await NoteCategory.objects.get_names(user)
    await call.message.edit_text(
        "Категории еще не добавлены" if not added_category_names
        else await format_user_added_values(added_category_names)
    )
    await call.message.edit_reply_markup(reply_markup=manage_categories_buttons)


@dp.callback_query_handler(text="add_category")
async def start_adding_category_process(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Введите название новой категории</b>\n\n"
        "Примеры 👇🏻\n<code>Английский</code>\n<code>Маркетинг</code>",
        reply_markup=cancel_button
    )
    await CategoryOperation.input_name.set()


async def _category_name_is_valid(name: str, category_names: Iterable[str]):
    return len(name) < 64 and (name not in category_names)


@dp.message_handler(content_types=["text"], state=CategoryOperation.input_name)
async def save_category(message: Message, user: User, state: FSMContext):
    added_category_names = await NoteCategory.objects.get_names(user)
    if not await _category_name_is_valid(message.text, added_category_names):
        return await message.answer(
            "<b>Название категории невалидно, введите заново\n\nТребования 👇🏻</b>\n"
            "✔️ Уникальность\n"
            "✔️ До 64 символов",
            reply_markup=cancel_button
        )
    
    await state.finish()
    await NoteCategory.objects.create(name=message.text, creator=user)
    await message.answer(
        "<b>Новая категория сохранена ✔️</b>\n"
        "Теперь к ней можно добавить заметки",
        reply_markup=manage_categories_buttons
    )


@dp.callback_query_handler(text="remove_category")
async def start_removing_category_process(call: CallbackQuery, user: User):
    user_categories = await user.categories.all()
    if not user_categories:
        return await call.message.edit_text(
            "Категории еще не добавлены",
            reply_markup=manage_categories_buttons
        )
    
    await call.message.edit_text(
        "Выберите категорию, которую хотите удалить",
        reply_markup=await categories_with_id_buttons(
            await user.categories.all(),
            choosing_for_removing_cb
        )
    )
    await CategoryOperation.choosing_for_removing.set()


@dp.callback_query_handler(choosing_for_removing_cb.filter(), state=CategoryOperation.choosing_for_removing)
async def remove_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = int(callback_data.get("category_id"))
    await NoteCategory.objects.delete(id=category_id)
    await call.message.edit_text(
        "<b>Категория была удалена ✔️</b>\n",
        reply_markup=manage_categories_buttons
    )
    await state.finish()
