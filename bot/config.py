from os import environ

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = environ.get("BOT_TOKEN")

DATABASE_URL = environ.get("DATABASE_URL")

YOOMONEY_TOKEN = environ.get("YOOMONEY_TOKEN")

APP_OVERVIEW_POST = environ.get("APP_OVERVIEW_POST")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())
