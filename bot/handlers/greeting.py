from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from buttons import user_home_buttons, try_app_button
from config import dp
from storage.models import User
from tools.texts import GREETING, INTRO


@dp.message_handler(commands=["start"], state="*")
async def greet_user(message: Message, user: User, state: FSMContext):
    await state.finish()
    
    if not user:
        return await message.answer(GREETING, reply_markup=try_app_button)
    
    await message.answer(
        f"<b>Хорошего дня, {message.from_user.first_name} 💎</b>",
        reply_markup=user_home_buttons
    )


@dp.callback_query_handler(text="try_app")
async def send_intro(call: CallbackQuery):
    await User.objects.get_or_create(tg_id=call.from_user.id)
    await call.message.delete_reply_markup()
    await call.message.answer(INTRO, reply_markup=user_home_buttons)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        f"<b>Хорошего дня, {call.from_user.first_name} 💎</b>",
        reply_markup=user_home_buttons
    )
