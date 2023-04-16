from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from storage.models import User


class UserAddingMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(message: Message, data: dict):
        user = await User.objects.get_or_none(tg_id=message.from_user.id)
        data["user"] = user
    
    @staticmethod
    async def on_pre_process_callback_query(message: Message, data: dict):
        user = await User.objects.get_or_none(tg_id=message.from_user.id)
        data["user"] = user
