from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from storage.models import User


class UserAddingMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(message: Message, data: dict):
        user = await User.objects.get_or_none(tg_id=message.from_user.id)
        data["user"] = user
    
    @staticmethod
    async def on_pre_process_callback_query(call: CallbackQuery, data: dict):
        user = await User.objects.get_or_none(tg_id=call.from_user.id)
        data["user"] = user


class ChatTypeIsPrivate(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict):
        if message.chat.type != "private":
            raise CancelHandler
    
    @staticmethod
    async def on_pre_process_callback_query(call: CallbackQuery, data: dict):
        if call.message.chat.type != "private":
            raise CancelHandler
