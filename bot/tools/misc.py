import random
from typing import Iterable

from config import bot


async def format_user_added_values(values: Iterable[str]):
    prefix = "• " if values else ""
    return prefix + "\n• ".join(values)


async def send_text_from_bot(tg_id: int, text: str, markup=None):
    try:
        await bot.send_message(tg_id, text, reply_markup=markup)
    except:
        return


async def choice_random_signature(signatures: tuple[str]) -> str:
    return random.choice(signatures)
