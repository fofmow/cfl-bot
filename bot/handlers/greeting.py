from aiogram.types import Message

from config import dp
from tools.texts import GREETING


@dp.message_handler(commands=["start"])
async def greet_user(message: Message):
    await message.answer(GREETING)
