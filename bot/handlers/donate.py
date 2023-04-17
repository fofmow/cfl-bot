import random
import string

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiomoney import YooMoneyWallet

from buttons import cancel_button, donate_button
from config import dp, YOOMONEY_TOKEN
from states import Donate


@dp.callback_query_handler(text="donate")
async def start_donating_process(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Благодарим за вашу лояльность!</b>\n\n"
        "Если вы готовы поддержать проект, введите в чат сумму доната",
        reply_markup=cancel_button
    )
    await Donate.input_amount.set()


@dp.message_handler(content_types=["text"], state=Donate.input_amount)
async def send_donate_invoice(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        return await message.answer(
            "<b>Кажется, Вы ввели нечисловое значение</b>\nПопробуйте снова 💎")
    
    if int(message.text) > 10000:
        return await message.answer(
            "<b>Донаты более 10000 ₽ не принимаются</b>\nУкажите значение меньше"
        )
    
    wallet = YooMoneyWallet(access_token=YOOMONEY_TOKEN)
    
    payment_form = await wallet.create_payment_form(
        amount_rub=int(message.text),
        unique_label=await _gen_random_label(),
        success_redirect_url="https://t.me/cfl_mind_bot"
    )
    await message.answer(
        "<b>Оплата принимается через провайдера ЮКасса</b>",
        reply_markup=await donate_button(payment_form.link_for_customer)
    )
    await state.finish()


async def _gen_random_label() -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.sample(chars, 10))
