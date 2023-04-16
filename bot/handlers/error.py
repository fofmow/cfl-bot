from aiogram.types import Update
from aiogram.utils.exceptions import MessageNotModified

from config import dp


@dp.errors_handler()
async def errors_handler(update: Update, exception):
    if isinstance(exception, MessageNotModified):
        return await update.callback_query.answer()
    
    print(exception)
